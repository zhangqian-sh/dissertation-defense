<script setup lang="ts">
import { computed } from 'vue'
import { useDefenseAsset,row } from '../composables/useDefenseAsset'
import { usePlayback } from '../composables/usePlayback'
const {payload:p,error,staticMode}=useDefenseAsset('ch02/sms_longtime_rollout')
const count=computed(()=>p.value?.time.shape[0]||100)
const {index,playing,toggle,seek,reset}=usePlayback(count,0,110)
const field=computed(()=>p.value?[{name:'Reference',color:'#232727',y:row(p.value.reference_state,index.value)},{name:'Teacher-forced',color:'#287e83',y:row(p.value.one_step_state,index.value)},{name:'Autoregressive',color:'#8b242d',y:row(p.value.cascade_state,index.value)}]:[])
const errors=computed(()=>p.value?[{name:'Teacher-forced',color:'#287e83',y:p.value.one_step_error.values},{name:'Autoregressive',color:'#8b242d',y:p.value.cascade_error.values}]:[])
</script>
<template>
<FigureFrame class="sms-rollout" fallback="/fallback_figures/ch02/sms_longtime_rollout.png" :ready="!!p" :error="error" :static-mode="staticMode" caption="">
  <div class="cols" style="gap:35px;height:320px">
    <div><div class="legend"><span v-for="s in field" :key="s.name" :style="{'--series':s.color}">{{s.name}}</span></div><TracePlot :axis-text-size="12" vertical-y-label :x="p.coordinates.values" :series="field" :min-y="0" :max-y="1" :width="500" :height="250" x-label="x" y-label="u" /></div>
    <div><div class="legend"><span v-for="s in errors" :key="s.name" :style="{'--series':s.color}">{{s.name}}</span></div><TracePlot :axis-text-size="12" vertical-y-label :x="p.time.values" :series="errors" :width="500" :height="250" :cursor="index" :boundary="p.training_end_time" x-label="physical time · s" y-label="relative L₂" @seek="seek" /></div>
  </div>
  <div class="plot-controls"><button @click="toggle">{{playing?'Pause':'Play'}}</button><button @click="reset">Reset</button><input class="playback-slider" :style="{'--progress': `${100*index/Math.max(1,count-1)}%`}" aria-label="SMS physical time" type="range" min="0" :max="count-1" :value="index" @input="seek(Number(($event.target as HTMLInputElement).value))"><output>{{p.time.values[index].toFixed(4)}} s</output></div>
</FigureFrame>
</template>

<style scoped>
.legend{font-size:16px}
.plot-controls{font-size:14px}
.sms-rollout :deep(.trace-svg text){font-size:12px}
.sms-rollout :deep(.trace-svg .trace-annotation){font-size:16px}

</style>
