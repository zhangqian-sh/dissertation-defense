<script setup lang="ts">
import {computed, onMounted, onBeforeUnmount, ref, watch} from 'vue'
import {useIsSlideActive, useNav} from '@slidev/client'
import {publicAssetUrl} from '../composables/publicAssetUrl.mjs'
const active = useIsSlideActive(), nav = useNav(), ready = ref(false), video = ref<HTMLVideoElement>()
const staticMode = computed(() => nav.isPrintMode.value || ['static', 'print'].some(key => new URLSearchParams(location.search).has(key)))
const source = publicAssetUrl('/figures/ch08/hide-seek/original.mp4')
const poster = publicAssetUrl('/figures/ch08/hide-seek/poster.png')
// Start after the title card; end before the outro montage.
const start = 6, end = 133.1
let motion: MediaQueryList | undefined, frame = 0, disposed = false
function stop() {
  if (frame && video.value) video.value.cancelVideoFrameCallback(frame)
  frame = 0; video.value?.pause()
}
function nextFrame() {
  const el = video.value
  if (!el || disposed) return
  if (el.currentTime >= end) el.currentTime = start
  frame = el.requestVideoFrameCallback(nextFrame)
}
function sync() {
  stop()
  const el = video.value
  if (!el || !ready.value) return
  if (el.currentTime < start || el.currentTime >= end) el.currentTime = start
  if (active.value && !staticMode.value && !motion?.matches && !document.hidden) {
    frame = el.requestVideoFrameCallback(nextFrame)
    void el.play().catch(() => {})
  }
}
function initialize() {
  if (video.value) video.value.currentTime = start
  ready.value = true; sync()
}
watch([active, staticMode], sync)
onMounted(() => {
  motion = matchMedia('(prefers-reduced-motion: reduce)'); motion.addEventListener('change', sync)
  document.addEventListener('visibilitychange', sync); sync()
})
onBeforeUnmount(() => {
  disposed = true; stop(); motion?.removeEventListener('change', sync)
  document.removeEventListener('visibilitychange', sync)
})
</script>
<template>
  <div class="hide-seek-figure" :data-ready="ready" role="img"
    aria-label="OpenAI hide-and-seek: complete demonstrations of agent interaction, tool use, and counterstrategies"
    title="OpenAI, Emergent Tool Use from Multi-Agent Interaction (2019); full strategy-demonstration sequence">
    <img v-if="staticMode" :src="poster" alt="OpenAI hide-and-seek agents interacting with boxes and ramps" @load="ready = true" />
    <video v-else ref="video" :src="source" :poster="poster" muted playsinline preload="auto" @loadeddata="initialize" />
  </div>
</template>
<style scoped>
.hide-seek-figure{position:relative;width:100%;height:160px;overflow:hidden}
.hide-seek-figure video,.hide-seek-figure img{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);width:100%;max-width:none;height:auto;aspect-ratio:16/9;object-fit:contain}
</style>
