<script setup lang="ts">
import {computed,onMounted,onBeforeUnmount,ref,watch} from 'vue'
import {useNav} from '@slidev/client'
import {usePlayback} from '../composables/usePlayback'
import {loadAnimationIndex,loadAnimationFrames} from '../composables/animationBundle.mjs'
const props=defineProps<{caseName:'vortex'|'jet';compact?:boolean}>()
const nav=useNav()
const staticMode=computed(()=>nav.isPrintMode.value||['static','print'].some(k=>new URLSearchParams(location.search).has(k)))
const data=ref<any>();const error=ref('');const urls=ref<string[]>([])
const count=computed(()=>data.value?.times.length||1)
const {index,playing,active,toggle,seek,reset}=usePlayback(count,0,250)
watch([active,data],()=>{if(props.caseName==='jet'&&active.value&&data.value&&!staticMode.value&&!document.hidden&&!playing.value)toggle()})
const fallback=computed(()=>error.value?`/figures/ch06/${props.caseName==='vortex'?'vortex':'jet'}-reconstruction.png`:`/fallback_figures/ch06/${props.caseName}.png`)
let disposed=false
onMounted(async()=>{
 if(staticMode.value)return
 try{
  const d=await loadAnimationIndex(props.caseName)
  if(d.frames.length!==d.times.length||!d.times.every((t:number,i:number)=>Number.isFinite(t)&&(!i||t>d.times[i-1])))throw Error('Invalid physical-time order')
  const loaded=await loadAnimationFrames(d)
  if(disposed){loaded.dispose();return}
  urls.value=loaded.frames.map((frame:string[])=>frame[0]);data.value=d
 }catch(e){if(!disposed)error.value=String(e)}
})
onBeforeUnmount(()=>{disposed=true;urls.value.forEach(u=>URL.revokeObjectURL(u))})
</script>
<template>
 <FigureFrame :class="{'vortex-matrix':caseName==='vortex','rformer-compact':compact,'rformer-jet':caseName==='jet'}" :fallback="fallback" :ready="!!data" :error="error" :static-mode="staticMode" :caption="caseName==='vortex'?'Rows: u / v / p · Columns: reference / observed / reconstructed · fixed row scales.':'Native (u,v) arrows · |z| < 5 slab · same reference/RFormer locations · fixed arrow scale.'">
  <img class="rformer-time-frame" :src="urls[index]" :alt="`Reference, observations and RFormer ${caseName==='vortex'?'u, v, p fields':'velocity vectors'} at physical-time ${data.times[index]}`">
  <div class="plot-controls"><button @click="toggle">{{playing?'Pause':'Play'}}</button><button @click="reset">Reset</button><label :for="'rformer-'+caseName">Physical time{{caseName==='jet'?' index':''}}</label><input :class="{'playback-slider':compact||caseName==='jet'}" :style="compact||caseName==='jet'?{'--progress':`${100*index/Math.max(1,count-1)}%`}:undefined" :id="'rformer-'+caseName" :aria-label="'RFormer '+caseName+' physical time'" type="range" min="0" :max="count-1" :value="index" @input="seek(Number(($event.target as HTMLInputElement).value))"><output><template v-if="!compact&&caseName!=='jet'">{{data.times[index]}} · </template>{{index+1}} / {{count}}</output></div>
  <div v-if="caseName!=='jet'" class="rformer-time-note">{{caseName==='jet'?'Saved test times are nonuniform; playback advances one recorded snapshot per frame. Time index is not seconds.':'Source time units · fixed color scales across all recorded times.'}}</div>
 </FigureFrame>
</template>
<style scoped>
.rformer-time-frame{width:100%;height:300px;object-fit:contain;display:block}
.vortex-matrix{height:440px}
.vortex-matrix .rformer-time-frame{height:355px}
.vortex-matrix :deep(.figure-fallback){height:400px}
.rformer-time-note{font-size:11px;color:#536160;margin-top:5px}
.plot-controls label,.plot-controls output{white-space:nowrap}
.rformer-compact{height:440px}
.rformer-compact .plot-controls{font-size:14px;gap:8px}
.rformer-compact .rformer-time-note{display:none}
.rformer-compact :deep(.interaction-note){display:none}
.rformer-jet{height:342px}
.rformer-jet :deep(.interaction-note){display:none}
.rformer-jet .plot-controls{font-size:14px;gap:8px}
</style>
