<script setup lang="ts">
import {computed,ref} from 'vue'
import {useDefenseAsset} from '../composables/useDefenseAsset'
import {usePlayback} from '../composables/usePlayback'
const {payload:p,error,staticMode}=useDefenseAsset('ch05/energy_history')
const count=computed(()=>p.value?.iteration.values.length||12)
const {index,playing,toggle,seek,reset}=usePlayback(count,0,600)
const showError=ref(false)
const current=computed(()=>{if(!p.value)return [];const n=p.value.reference.values.length;return p.value.frames.values.subarray(index.value*n,(index.value+1)*n)})
const residual=computed(()=>Float64Array.from(current.value,(v,i)=>v-p.value.reference.values[i]))
const bounds=computed(()=>p.value?p.value.reference.values.reduce((a,v)=>[Math.min(a[0],v),Math.max(a[1],v)],[Infinity,-Infinity]):[-1,1])
const center=computed(()=>(bounds.value[0]+bounds.value[1])/2)
const limit=computed(()=>(bounds.value[1]-bounds.value[0])/2)
const outside=computed(()=>current.value.length?100*Array.from(current.value).filter(v=>v<bounds.value[0]||v>bounds.value[1]).length/current.value.length:0)
const maskLimit=computed(()=>p.value?.masked.values.reduce((m,v)=>Math.max(m,Math.abs(v)),0)||1)
const errorLimit=computed(()=>p.value?.frames.values.reduce((m,v,i)=>Math.max(m,Math.abs(v-p.value.reference.values[i%p.value.reference.values.length])),0)||1)
</script>
<template>
<FigureFrame fallback="/fallback_figures/ch05/energy_history.png" :ready="!!p" :error="error" :static-mode="staticMode" caption="Vortex v · 90% nominal masking · α=0.1 · 12 updates · native unsmoothed pixels · fixed reference-range colors; saturation outside range · scroll to step.">
 <div class="energy-fields" @wheel.prevent="seek(index+($event.deltaY>0?1:-1))">
  <GridField :values="p.reference.values" :rows="p.reference.shape[0]" :cols="p.reference.shape[1]" :limit="limit" :center="center" title="Reference · normalized v"/>
  <GridField :values="p.masked.values" :rows="p.reference.shape[0]" :cols="p.reference.shape[1]" :limit="maskLimit" title="Saved masked input · own scale"/>
  <GridField :values="showError?residual:current" :rows="p.reference.shape[0]" :cols="p.reference.shape[1]" :limit="showError?errorLimit:limit" :center="showError?0:center" :title="`${showError?'Error':'Update '+(index+1)} · ${showError?'fixed scale':outside.toFixed(1)+'% outside color range'}`"/>
 </div>
 <div class="energy-traces">
  <TracePlot :x="p.iteration.values" :series="[{name:'Field error',color:'#8b242d',y:p.relative_error.values}]" :cursor="index" :width="500" :height="105" x-label="token update" y-label="v-field relative L₂" @seek="seek($event)"/>
  <TracePlot :x="p.iteration.values" :series="[{name:'Energy',color:'#287e83',y:p.energy.values}]" :cursor="index" :min-y="Math.min(...p.energy.values)" :max-y="Math.max(...p.energy.values)" :width="500" :height="105" x-label="token update" y-label="full-system learned energy" @seek="seek($event)"/>
 </div>
 <div class="plot-controls"><button @click="toggle">{{playing?'Pause':'Play'}}</button><button @click="reset">Reset</button><input aria-label="ET reconstruction iteration" type="range" min="0" :max="count-1" :value="index" @input="seek(Number(($event.target as HTMLInputElement).value))"><output>Update {{index+1}} / {{count}}</output><label><input type="checkbox" v-model="showError"> Show error</label></div>
</FigureFrame>
</template>
