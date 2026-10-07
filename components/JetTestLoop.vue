<script setup lang="ts">
import {computed,onMounted,onBeforeUnmount,ref,watch} from 'vue'
import {useIsSlideActive,useNav} from '@slidev/client'
import {publicAssetUrl} from '../composables/publicAssetUrl.mjs'

const active=useIsSlideActive(),nav=useNav()
const staticMode=computed(()=>nav.isPrintMode.value||['static','print'].some(k=>new URLSearchParams(location.search).has(k)))
const ready=ref(false),index=ref(0),playing=ref(true),scrubbing=ref(false)
const channels=['u','v','p'],columns=['Original','Masked','Reconstructed']
const canvases:HTMLCanvasElement[]=[]
let values:Float32Array,metadata:any,timer:ReturnType<typeof setInterval>|undefined,disposed=false
function draw(){
 if(!ready.value)return
 for(let c=0;c<3;c++)for(let column=0;column<3;column++){
  const canvas=canvases[c*3+column];if(!canvas)continue
  const pixels=new Uint8ClampedArray(48*32*4),offset=((index.value*3+c)*3+column)*48*32
  const [low,high]=metadata.limits[c]
  for(let i=0;i<48*32;i++){
   const paletteIndex=Math.round(Math.max(0,Math.min(1,(values[offset+i]-low)/(high-low)))*255)
   pixels.set(metadata.palette[paletteIndex],4*i);pixels[4*i+3]=255
  }
  canvas.getContext('2d')!.putImageData(new ImageData(pixels,48,32),0,0)
 }
}
function syncPlayback(){
 if(timer)clearInterval(timer);timer=undefined
 if(ready.value&&playing.value&&!scrubbing.value&&active.value&&!staticMode.value&&!document.hidden)
  timer=setInterval(()=>{index.value=(index.value+1)%40;draw()},metadata.frame_interval_ms)
}
function seek(event:Event){
 index.value=Math.max(0,Math.min(39,Number((event.target as HTMLInputElement).value)))
 draw()
}
watch([active,staticMode,ready,playing,scrubbing],syncPlayback)
onMounted(async()=>{
 document.addEventListener('visibilitychange',syncPlayback)
 if(staticMode.value)return
 try{
  const r=await fetch(publicAssetUrl('/data/ch05/jet-test/index.json'));if(!r.ok)throw Error('Missing jet sequence')
  const m=await r.json()
  if(JSON.stringify(m.shape)!=='[40,3,3,32,48]'||m.limits.length!==3||m.palette.length!==256||m.frame_interval_ms!==150)throw Error('Invalid jet sequence')
  const frames=await fetch(publicAssetUrl('/data/ch05/jet-test/frames.bin'));if(!frames.ok)throw Error('Missing jet frames')
  const bytes=await frames.arrayBuffer()
  const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))).map(v=>v.toString(16).padStart(2,'0')).join('')
  if(hash!==m.sha256||bytes.byteLength!==40*3*3*48*32*4)throw Error('Invalid jet frame data')
  const decoded=new Float32Array(bytes);if(!decoded.every(Number.isFinite))throw Error('Nonfinite jet data')
  if(disposed)return
  metadata=m;values=decoded;ready.value=true
  // Canvas refs mount on the next Vue update.
 }catch(e){console.error('Jet playback: using published static panels',e)}
})
watch(ready,()=>requestAnimationFrame(draw),{flush:'post'})
onBeforeUnmount(()=>{disposed=true;if(timer)clearInterval(timer);document.removeEventListener('visibilitychange',syncPlayback)})
</script>

<template>
 <div v-if="ready&&!staticMode" class="jet-test-loop">
 <div class="jet-test-grid" role="img" :aria-label="`Turbulent jet test snapshot ${160+index}: rows u, v, p; columns original, masked input, reconstruction`">
  <template v-for="(channel,c) in channels" :key="channel">
   <div v-for="(column,k) in columns" :key="column" class="jet-test-panel">
    <div class="jet-test-title">{{column}} <i>{{channel}}</i></div>
    <div class="jet-test-axes">
     <canvas :ref="el=>{if(el)canvases[c*3+k]=el as HTMLCanvasElement}" width="48" height="32"/>
     <span v-for="tick in [0,10,20,30,40]" :key="'x'+tick" class="jet-test-x" :style="{left:`${100*(tick+.5)/48}%`}">{{tick}}</span>
     <span v-for="tick in [0,10,20,30]" :key="'y'+tick" class="jet-test-y" :style="{top:`${100*(tick+.5)/32}%`}">{{tick}}</span>
    </div>
   </div>
  </template>
 </div>
 <div class="plot-controls jet-test-controls">
  <button @click="playing=!playing">{{playing?'Pause':'Play'}}</button>
  <input class="playback-slider" type="range" min="0" max="39" :value="index" :style="{'--progress':`${100*index/39}%`}" aria-label="Turbulent jet test snapshot" @input="seek" @pointerdown="scrubbing=true" @pointerup="scrubbing=false" @pointercancel="scrubbing=false" @blur="scrubbing=false">
  <output>{{index+1}} / 40</output>
 </div>
 </div>
 <div v-else class="jet-test-fallback">
  <img v-for="channel in channels" :key="channel" :src="publicAssetUrl(`/figures/ch05/et-3djet-results-${channel}.png`)" :alt="`${channel}: original, masked input and reconstruction`"/>
 </div>
</template>

<style scoped>
.jet-test-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));grid-template-rows:repeat(3,150px);column-gap:16px}
.jet-test-controls{font-size:14px;height:32px;padding-top:4px;margin-bottom:4px}
.jet-test-controls output{min-width:76px}
.jet-test-panel{min-width:0;padding-left:24px;padding-right:4px}
.jet-test-title{font-size:12px;text-align:center;height:24px;line-height:20px;white-space:nowrap}
.jet-test-axes{position:relative;height:110px;border:1px solid #596361}
.jet-test-axes canvas{display:block;width:100%;height:100%;image-rendering:pixelated}
.jet-test-x,.jet-test-y{position:absolute;font-size:12px;line-height:16px}
.jet-test-x{top:100%;margin-top:2px;transform:translateX(-50%)}
.jet-test-y{right:100%;margin-right:4px;transform:translateY(-50%)}
.jet-test-fallback{display:grid;gap:0}
.jet-test-fallback img{display:block;width:100%;height:155px;object-fit:contain}
</style>
