<script setup lang="ts">
import {computed,onMounted,onBeforeUnmount,ref} from 'vue'
import {useNav} from '@slidev/client'
import {usePlayback} from '../composables/usePlayback'
import {publicAssetUrl} from '../composables/publicAssetUrl.mjs'
const props=defineProps<{caseName:'vortex'|'jet'}>()
const nav=useNav()
const staticMode=computed(()=>nav.isPrintMode.value||['static','print'].some(k=>new URLSearchParams(location.search).has(k)))
const data=ref<any>();const error=ref('');const urls=ref<string[]>([])
const count=computed(()=>data.value?.times.length||1)
const {index,playing,toggle,seek,reset}=usePlayback(count,0,250)
const fallback=computed(()=>error.value?`/figures/ch06/${props.caseName==='vortex'?'vortex':'jet'}-reconstruction.png`:`/data/ch06/time/${props.caseName}-000.png`)
let disposed=false
onMounted(async()=>{
 if(staticMode.value)return
 try{
  const response=await fetch(publicAssetUrl(`/data/ch06/time/${props.caseName}.json`))
  if(!response.ok)throw Error('Missing time sequence')
  const d=await response.json()
  if(d.frames.length!==d.times.length||!d.times.every((t:number,i:number)=>Number.isFinite(t)&&(!i||t>d.times[i-1])))throw Error('Invalid physical-time order')
  const loaded=await Promise.all(d.frames.map(async(f:any)=>{
   if(!f.path.startsWith('/data/ch06/time/'))throw Error('Nonlocal frame')
   const r=await fetch(publicAssetUrl(f.path));if(!r.ok)throw Error('Missing frame')
   const bytes=await r.arrayBuffer()
   const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))).map(v=>v.toString(16).padStart(2,'0')).join('')
   if(hash!==f.sha256)throw Error('Frame checksum mismatch')
   return new Blob([bytes],{type:'image/png'})
  }))
  if(disposed)return
  urls.value=loaded.map(b=>URL.createObjectURL(b));data.value=d
 }catch(e){if(!disposed)error.value=String(e)}
})
onBeforeUnmount(()=>{disposed=true;urls.value.forEach(u=>URL.revokeObjectURL(u))})
</script>
<template>
 <FigureFrame :class="{'vortex-matrix':caseName==='vortex'}" :fallback="fallback" :ready="!!data" :error="error" :static-mode="staticMode" :caption="caseName==='vortex'?'u / v / p · 512 observations · reference / observed / reconstructed · row scales fixed across time.':'Native (u,v) arrows · |z| < 5 slab · same reference/RFormer locations · fixed arrow scale.'">
  <img class="rformer-time-frame" :src="urls[index]" :alt="`Reference, observations and RFormer ${caseName==='vortex'?'u, v, p fields':'velocity vectors'} at physical-time ${data.times[index]}`">
  <div class="plot-controls"><button @click="toggle">{{playing?'Pause':'Play'}}</button><button @click="reset">Reset</button><label :for="'rformer-'+caseName">Physical time{{caseName==='jet'?' index':''}}</label><input :id="'rformer-'+caseName" :aria-label="'RFormer '+caseName+' physical time'" type="range" min="0" :max="count-1" :value="index" @input="seek(Number(($event.target as HTMLInputElement).value))"><output>{{data.times[index]}} · {{index+1}} / {{count}}</output></div>
  <div class="rformer-time-note">{{caseName==='jet'?'Saved test times are nonuniform; playback advances one recorded snapshot per frame. Time index is not seconds.':'Source time units · fixed color scales across all recorded times.'}}</div>
 </FigureFrame>
</template>
<style scoped>
.rformer-time-frame{width:100%;height:300px;object-fit:contain;display:block}
.vortex-matrix{height:440px}
.vortex-matrix .rformer-time-frame{height:355px}
.vortex-matrix :deep(.figure-fallback){height:400px}
.rformer-time-note{font-size:11px;color:#536160;margin-top:5px}
.plot-controls label,.plot-controls output{white-space:nowrap}
</style>
