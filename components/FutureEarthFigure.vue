<script setup lang="ts">
import {computed, onBeforeUnmount, onMounted, ref, watch} from 'vue'
import {useIsSlideActive, useNav} from '@slidev/client'
import {publicAssetUrl} from '../composables/publicAssetUrl.mjs'

const video = ref<HTMLVideoElement>(), canvas = ref<HTMLCanvasElement>(), ready = ref(false)
const active = useIsSlideActive(), nav = useNav()
const staticMode = computed(() => nav.isPrintMode.value || ['static', 'print'].some(key => new URLSearchParams(location.search).has(key)))
const source = publicAssetUrl('/figures/ch08/earth/nasa-earth.mp4')
const poster = publicAssetUrl('/figures/ch08/earth/nasa-poster.jpg')
let motion: MediaQueryList | undefined, observer: ResizeObserver | undefined
let buffer: HTMLCanvasElement, context: CanvasRenderingContext2D
let still: HTMLImageElement, callback = 0, lastFrame = -Infinity, disposed = false

function draw(input: CanvasImageSource) {
  const el = canvas.value
  if (!el || !context || !el.clientWidth) return
  // Give the full observed Earth disk a larger circular space backdrop.
  // A feathered outer edge blends the black surround into the white slide.
  context.clearRect(0, 0, 512, 512)
  context.globalCompositeOperation = 'source-over'
  context.fillStyle = '#000'; context.fillRect(0, 0, 512, 512)
  context.drawImage(input, 0, 112, 512, 288)
  const fade = context.createRadialGradient(262, 256, 154, 262, 256, 180)
  fade.addColorStop(0, 'rgba(0,0,0,1)')
  fade.addColorStop(.5, 'rgba(0,0,0,.55)')
  fade.addColorStop(1, 'rgba(0,0,0,0)')
  context.globalCompositeOperation = 'destination-in'
  context.fillStyle = fade; context.fillRect(0, 0, 512, 512)
  context.globalCompositeOperation = 'source-over'
  const w = el.clientWidth, h = el.clientHeight, dpr = Math.min(devicePixelRatio || 1, 2)
  if (el.width !== Math.round(w * dpr) || el.height !== Math.round(h * dpr)) {
    el.width = Math.round(w * dpr); el.height = Math.round(h * dpr)
  }
  const out = el.getContext('2d')!
  out.setTransform(dpr, 0, 0, dpr, 0, 0); out.clearRect(0, 0, w, h)
  out.drawImage(buffer, 82, 76, 360, 360, (w - h) / 2, 0, h, h)
  ready.value = true
}
function currentFrame() {
  if (video.value && video.value.readyState >= 2) draw(video.value)
  else if (still?.complete && still.naturalWidth) draw(still)
}
function stop() {
  if (callback && video.value) video.value.cancelVideoFrameCallback(callback)
  callback = 0; video.value?.pause(); lastFrame = -Infinity
}
function nextFrame(now: number) {
  // Keep the previous canvas image across the loop boundary: no blank flash.
  if (now - lastFrame >= 30) {
    currentFrame(); lastFrame = now
    if (canvas.value && video.value) canvas.value.dataset.time = String(video.value.currentTime)
  }
  if (!disposed && video.value) callback = video.value.requestVideoFrameCallback(nextFrame)
}
function sync() {
  stop(); currentFrame()
  const el = video.value
  if (el && active.value && !staticMode.value && !document.hidden && !motion?.matches) {
    el.playbackRate = 2
    callback = el.requestVideoFrameCallback(nextFrame)
    void el.play().catch(() => {})
  }
}
watch([active, staticMode], sync)
onMounted(() => {
  buffer = document.createElement('canvas'); buffer.width = 512; buffer.height = 512
  context = buffer.getContext('2d')!
  still = new Image(); still.onload = () => { if (!disposed) currentFrame() }; still.src = poster
  motion = matchMedia('(prefers-reduced-motion: reduce)'); motion.addEventListener('change', sync)
  observer = new ResizeObserver(currentFrame); if (canvas.value) observer.observe(canvas.value)
  document.addEventListener('visibilitychange', sync); sync()
})
onBeforeUnmount(() => {
  disposed = true; stop(); observer?.disconnect(); still.onload = null
  document.removeEventListener('visibilitychange', sync); motion?.removeEventListener('change', sync)
})
</script>
<template>
  <div class="earth-figure" :data-ready="ready" role="img"
    aria-label="Continuously rotating Earth in a circular black space backdrop softly fading into white"
    title="NASA Scientific Visualization Studio; Kel Elkins (USRA), Blue Marble imagery by Reto Stockli (NASA/GSFC)">
    <canvas ref="canvas" class="earth-canvas" />
    <video v-if="!staticMode" ref="video" class="earth-source" :src="source"
      muted loop playsinline preload="auto" aria-hidden="true" @loadeddata="sync" />
  </div>
</template>
<style scoped>
.earth-figure{position:relative;width:100%;height:160px;overflow:hidden;background:white}
.earth-canvas{display:block;width:100%;height:100%}
.earth-source{position:absolute;width:1px;height:1px;opacity:0;pointer-events:none}
</style>
