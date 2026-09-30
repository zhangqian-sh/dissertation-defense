<script setup lang="ts">
import {computed,onMounted,onBeforeUnmount,ref} from 'vue'
import {useNav} from '@slidev/client'
import {usePlayback} from '../composables/usePlayback'
const props=defineProps<{name:string;label:string;caption:string}>()
const nav=useNav();const data=ref<any>();const urls=ref<string[]>([]);const error=ref('')
const staticMode=computed(()=>nav.isPrintMode.value||['static','print'].some(k=>new URLSearchParams(location.search).has(k)))
const count=computed(()=>data.value?.frames.length||1)
const {index,playing,toggle,seek,reset}=usePlayback(count,0,100)
let disposed=false
onMounted(async()=>{
 if(staticMode.value)return
 try{
  const r=await fetch(`/data/sequences/${props.name}/index.json`);if(!r.ok)throw Error('Missing sequence')
  const d=await r.json()
  if(d.frames.length!==d.times.length||d.labels.length!==d.times.length||!d.times.every((v:number,i:number)=>Number.isFinite(v)&&(!i||v>d.times[i-1])))throw Error('Invalid time sequence')
  const blobs=await Promise.all(d.frames.map(async(f:any)=>{
   if(!f.path.startsWith(`/data/sequences/${props.name}/`))throw Error('Unexpected frame path')
   const r=await fetch(f.path);if(!r.ok)throw Error('Missing frame');const bytes=await r.arrayBuffer()
   const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))).map(v=>v.toString(16).padStart(2,'0')).join('')
   if(hash!==f.sha256)throw Error('Frame checksum mismatch')
   return new Blob([bytes],{type:'image/png'})
  }))
  if(disposed)return;urls.value=blobs.map(b=>URL.createObjectURL(b));data.value=d
 }catch(e){if(!disposed)error.value=String(e)}
})
onBeforeUnmount(()=>{disposed=true;urls.value.forEach(URL.revokeObjectURL)})
</script>
<template>
 <FigureFrame :class="{'sequence-weather':name==='weather'}" :fallback="`/fallback_figures/sequences/${name}.png`" :ready="!!data" :error="error" :static-mode="staticMode" :caption="caption">
  <img class="recorded-frame" :src="urls[index]" :alt="label+' · '+data.labels[index]">
  <div class="plot-controls"><button @click="toggle">{{playing?'Pause':'Play'}}</button><button @click="reset">Reset</button><input :aria-label="label" type="range" min="0" :max="count-1" :value="index" @input="seek(Number(($event.target as HTMLInputElement).value))"><output>{{data.labels[index]}}</output></div>
 </FigureFrame>
</template>
<style scoped>
.recorded-frame{width:100%;height:310px;object-fit:contain;display:block}
.sequence-weather{height:445px}
.sequence-weather .recorded-frame{height:365px}
.sequence-weather :deep(.figure-fallback){height:400px}
.plot-controls{gap:8px}.plot-controls output{min-width:95px;font-size:11px}
</style>
