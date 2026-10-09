<script setup lang="ts">
import {ref,computed,onMounted,onBeforeUnmount,watch} from 'vue'
import {useIsSlideActive,useNav} from '@slidev/client'
import { publicAssetUrl } from '../composables/publicAssetUrl.mjs'
import {loadAnimationIndex,loadAnimationFrames} from '../composables/animationBundle.mjs'
const active=useIsSlideActive(),nav=useNav()
const staticMode=computed(()=>nav.isPrintMode.value||(typeof location!=='undefined'&&['static','print'].some(k=>new URLSearchParams(location.search).has(k))))
const metrics=ref<any>(null)
const formatMetric=(m:any)=>`${m.mean.toFixed(4)} ± ${m.std.toFixed(4)}`
const index=ref(0),frames=ref<string[][]>([])
let timer:ReturnType<typeof setInterval>|undefined,disposed=false
const stop=()=>{if(timer)clearInterval(timer);timer=undefined}
const sync=()=>{stop();if(frames.value.length&&active.value&&!staticMode.value&&!document.hidden)timer=setInterval(()=>{index.value=(index.value+1)%frames.value.length},250)}
const source=(component:string,col:number)=>frames.value.length&&!staticMode.value?frames.value[index.value][(component==='u'?0:4)+col]:publicAssetUrl(`/figures/ch06/blood-${component}-${col}.png`)
const visibility=()=>sync()
watch([active,staticMode],()=>{if(typeof document!=='undefined')sync()})
onMounted(async()=>{
 document.addEventListener('visibilitychange',visibility)
 try{
  const d=await loadAnimationIndex('blood');metrics.value=d.metrics
  if(staticMode.value||disposed)return
  if(d.frames.length!==20||d.frame_interval_ms!==250)throw Error('Invalid blood sequence')
  d.frames.forEach((f:any,k:number)=>{if(f.raw_index!==k||f.averaged_index!==80+k||f.panels.length!==8)throw Error('Invalid matched frame')})
  const loaded=await loadAnimationFrames(d,{decode:true})
  if(disposed){loaded.dispose();return}
  frames.value=loaded.frames;sync()
 }catch(e){console.warn('Blood animation: using static snapshot',e)}
})
onBeforeUnmount(()=>{disposed=true;stop();document.removeEventListener('visibilitychange',visibility);frames.value.flat().forEach(URL.revokeObjectURL)})
const headings=['Sparse observations','Linear interpolation','RFormer reconstruction','Averaged-grid reference']
const rows=['u','v']
const xticks=[{label:'0',position:100*6/312},{label:'150',position:50},{label:'300',position:100*306/312}]
const yticks=[{label:'50',position:100*4/108},{label:'0',position:50},{label:'−50',position:100*104/108}]
</script>
<template>
 <div class="blood-snapshot-grid" :aria-label="frames.length&&!staticMode?`Blood reconstruction frame ${index+1} of ${frames.length}`:'Blood reconstruction static snapshot'">
  <div class="blood-column-headings"><span></span><strong v-for="heading in headings" :key="heading">{{heading}}</strong></div>
  <div v-for="component in rows" :key="component" class="blood-snapshot-row">
   <div class="blood-component"><InlineMath :tex="component" /></div>
   <div v-for="(heading,i) in headings" :key="i" class="blood-panel">
    <div class="blood-data-box">
     <img :src="source(component,i)" :alt="`${component} velocity: ${heading}; same snapshot and component color limits across all four columns`">
     <template v-if="i===0"><span v-for="tick in yticks" :key="tick.label" class="blood-y-tick" :style="{top:tick.position+'%'}">{{tick.label}}</span><span class="blood-y-label"><InlineMath tex="y" /></span></template>
    </div>
    <div class="blood-x-ticks"><span v-for="tick in xticks" :key="tick.label" :style="{left:tick.position+'%'}">{{tick.label}}</span></div>
    <div class="blood-x-label"><InlineMath tex="x" /></div>
   </div>
  </div>
  <p class="blood-metrics">In this 3D dissipative particle dynamics (DPD) simulation, RFormer reconstructs 290,000 query points from 10,000 observed points (3.3%) per snapshot. The plots show midplane velocities (<InlineMath tex="|z|<1" />), with <InlineMath tex="u" /> above and <InlineMath tex="v" /> below. Both RFormer and sparse-observation linear interpolation (nearest-neighbor fill outside the observation hull) are compared with the averaged-grid reference.<template v-if="metrics"> Across 20 snapshots, 3D velocity relative <InlineMath tex="L^2" /> is <strong>{{formatMetric(metrics.methods.interpolation)}}</strong> for interpolation and <strong>{{formatMetric(metrics.methods.rformer)}}</strong> for RFormer (mean ± std), indicating closer agreement with the averaged field.</template></p>
 </div>
</template>
<style scoped>
.blood-metrics{font-size:14px;line-height:1.45;margin:0}
.blood-column-headings,.blood-snapshot-row{display:grid;grid-template-columns:40px repeat(4,minmax(0,1fr));gap:12px;align-items:center}
.blood-column-headings{margin-bottom:20px}
.blood-column-headings strong{font-size:16px;line-height:1.3;font-weight:600;text-align:center}
.blood-snapshot-row{padding:18px 0;margin-bottom:24px}
.blood-panel{min-width:0}
.blood-data-box{position:relative;border-left:1px solid #596361;border-bottom:1px solid #596361;aspect-ratio:312/108}
.blood-data-box img{display:block;width:100%;height:100%;object-fit:contain}
.blood-y-tick{position:absolute;right:calc(100% + 6px);transform:translateY(-50%);font-size:12px;white-space:nowrap}
.blood-y-label{position:absolute;right:calc(100% + 34px);top:50%;transform:translateY(-50%) rotate(-90deg);font-size:12px}
.blood-x-ticks{position:relative;height:21px;margin-top:4px;font-size:12px}
.blood-x-ticks span{position:absolute;transform:translateX(-50%)}
.blood-x-label{font-size:12px;text-align:center}
.blood-component{font-size:16px;text-align:left;align-self:start}
</style>
