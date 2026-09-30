<script setup lang="ts">
import { computed,ref } from 'vue'
import { useDefenseAsset,row } from '../composables/useDefenseAsset'
import { usePlayback } from '../composables/usePlayback'
const {payload:p,error,staticMode}=useDefenseAsset('ch02/sms_longtime_rollout')
const count=computed(()=>p.value?.time.shape[0]||100)
const {index,playing,toggle,seek,reset}=usePlayback(count,40,110)
const level=ref(2)
const field=computed(()=>p.value?[{name:'Reference',color:'#232727',y:row(p.value.reference_state,index.value)},{name:'Reference-fed',color:'#287e83',y:row(p.value.one_step_state,index.value)},{name:'Cascade',color:'#8b242d',y:row(p.value.cascade_state,index.value)}]:[])
const errors=computed(()=>p.value?[{name:'Reference-fed',color:'#287e83',y:p.value.one_step_error.values},{name:'Cascade',color:'#8b242d',y:p.value.cascade_error.values}]:[])
const codec=computed(()=>{if(!p.value)return [];const t=p.value.T_approximation;const offset=(level.value*count.value+index.value)*101;return [{name:'Reference',color:'#232727',y:row(p.value.reference_state,index.value)},{name:'Codec',color:'#b27a29',y:t.values.subarray(offset,offset+101)}]})
</script>
<template>
<FigureFrame fallback="/fallback_figures/ch02/sms_longtime_rollout.png" :ready="!!p" :error="error" :static-mode="staticMode" caption="Heat equation · K=100 · first two frames initialized · selected-T codec views are illustrative, not retrained models.">
  <div class="three" style="gap:20px;height:300px">
    <div><div class="chart-label">Temperature field</div><div class="legend"><span v-for="s in field" :key="s.name" :style="{'--series':s.color}">{{s.name}}</span></div><TracePlot :x="p.coordinates.values" :series="field" x-label="x · benchmark units" y-label="temperature" /></div>
    <div><div class="chart-label">Accumulated prediction error</div><div class="legend"><span v-for="s in errors" :key="s.name" :style="{'--series':s.color}">{{s.name}}</span></div><TracePlot :x="p.time.values" :series="errors" :cursor="index" :boundary="p.training_end_time" x-label="physical time · s" y-label="relative L₂" @seek="seek" /></div>
    <div><div class="chart-label">Codec approximation · illustrative</div><div class="legend"><span style="--series:#232727">Reference</span><span style="--series:#b27a29">T={{p.selected_T.values[level]}}</span></div><TracePlot :x="p.coordinates.values" :series="codec" x-label="x · benchmark units" y-label="decoded field" /></div>
  </div>
  <div class="plot-controls"><button @click="toggle">{{playing?'Pause':'Play'}}</button><button @click="reset">Reset</button><input aria-label="SMS physical time" type="range" min="0" :max="count-1" :value="index" @input="seek(Number(($event.target as HTMLInputElement).value))"><output>{{p.time.values[index].toFixed(4)}} s</output><label for="codec-t">Codec T</label><select id="codec-t" v-model.number="level"><option v-for="(t,i) in Array.from(p.selected_T.values)" :key="i" :value="i">{{t}}</option></select></div>
</FigureFrame>
</template>
