<script setup lang="ts">
import { computed } from 'vue'
import { useDefenseAsset,row } from '../composables/useDefenseAsset'
import { usePlayback } from '../composables/usePlayback'
const {payload:p,error,staticMode}=useDefenseAsset('ch02/sms_longtime_rollout')
const count=computed(()=>p.value?.time.shape[0]||100)
const {index,playing,toggle,seek,reset}=usePlayback(count,0,110)
const field=computed(()=>p.value?[{name:'Reference',color:'#232727',y:row(p.value.reference_state,index.value)},{name:'Reference-fed',color:'#287e83',y:row(p.value.one_step_state,index.value)},{name:'Cascade',color:'#8b242d',y:row(p.value.cascade_state,index.value)}]:[])
const errors=computed(()=>p.value?[{name:'Reference-fed',color:'#287e83',y:p.value.one_step_error.values},{name:'Cascade',color:'#8b242d',y:p.value.cascade_error.values}]:[])
</script>
<template>
<FigureFrame fallback="/fallback_figures/ch02/sms_longtime_rollout.png" :ready="!!p" :error="error" :static-mode="staticMode" caption="Heat equation · K=100 · first two frames initialized · reference-fed and recursive cascade predictions.">
  <div class="cols" style="gap:35px;height:320px">
    <div><div class="chart-label">Temperature field</div><div class="legend"><span v-for="s in field" :key="s.name" :style="{'--series':s.color}">{{s.name}}</span></div><TracePlot :x="p.coordinates.values" :series="field" :width="500" :height="250" x-label="x · benchmark units" y-label="temperature" /></div>
    <div><div class="chart-label">Accumulated prediction error</div><div class="legend"><span v-for="s in errors" :key="s.name" :style="{'--series':s.color}">{{s.name}}</span></div><TracePlot :x="p.time.values" :series="errors" :width="500" :height="250" :cursor="index" :boundary="p.training_end_time" x-label="physical time · s" y-label="relative L₂" @seek="seek" /></div>
  </div>
  <div class="plot-controls"><button @click="toggle">{{playing?'Pause':'Play'}}</button><button @click="reset">Reset</button><input aria-label="SMS physical time" type="range" min="0" :max="count-1" :value="index" @input="seek(Number(($event.target as HTMLInputElement).value))"><output>{{p.time.values[index].toFixed(4)}} s</output></div>
</FigureFrame>
</template>
