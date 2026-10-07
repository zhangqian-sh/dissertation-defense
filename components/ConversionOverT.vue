<script setup lang="ts">
import {computed} from 'vue'
import {useDefenseAsset} from '../composables/useDefenseAsset'
import {usePlayback} from '../composables/usePlayback'
const {payload:p,error,staticMode}=useDefenseAsset('ch03/conversion_over_t')
const count=computed(()=>p.value?.T.values.length||128)
const {index,playing,toggle,seek,reset}=usePlayback(count,0,100)
const current=computed(()=>{if(!p.value)return [];const n=p.value.reference.values.length;return p.value.frames.values.subarray(index.value*n,(index.value+1)*n)})
const difference=computed(()=>Float32Array.from(current.value,(v,i)=>v-p.value.reference.values[i]))
</script>
<template>
<FigureFrame fallback="/fallback_figures/ch03/conversion_over_t.png" :ready="!!p" :error="error" :static-mode="staticMode" caption="Burgers · spike averages for T=1–128 · calibration fixed at T=128 · T counts spike steps, not physical time.">
 <div class="burgers-fields">
  <GridField :values="p.reference.values" :rows="201" :cols="300" :limit="1" title="Reference"/>
  <GridField :values="current" :rows="201" :cols="300" :limit="1" :title="'SNN · T = '+p.T.values[index]"/>
  <GridField :values="difference" :rows="201" :cols="300" :limit="1" title="Difference · SNN − reference"/>
 </div>
 <div class="burgers-axis"><span>horizontal: x · vertical: physical t</span><span>horizontal: x · vertical: physical t</span><span>horizontal: x · vertical: physical t</span></div>
 <div class="burgers-readout"><span>Relative L₂: {{p.relative_error.values[index].toFixed(4)}}</span><span>Output = mean of emitted spikes 1…T · fixed weights / thresholds</span></div>
 <div class="plot-controls"><button @click="toggle">{{playing?'Pause':'Play'}}</button><button @click="reset">Reset</button><label for="burgers-t">T</label><input class="playback-slider" :style="{'--progress': `${100*index/Math.max(1,count-1)}%`}" id="burgers-t" aria-label="Burgers SNN T" type="range" min="0" :max="count-1" :value="index" @input="seek(Number(($event.target as HTMLInputElement).value))"><output>{{index+1}} / {{count}}</output><button v-for="t in [1,32,64,96,128]" :key="t" :aria-pressed="index===t-1" @click="seek(t-1)">T={{t}}</button></div>
</FigureFrame>
</template>

<style scoped>
.plot-controls{font-size:14px}
</style>
