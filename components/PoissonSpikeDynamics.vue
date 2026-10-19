<script setup lang="ts">
import { computed } from 'vue'
import 'katex/dist/katex.min.css'
import { useDefenseAsset } from '../composables/useDefenseAsset'
import { usePlayback } from '../composables/usePlayback'
import FigureFrame from './FigureFrame.vue'
import GridField from './GridField.vue'
import InlineMath from './InlineMath.vue'

const { payload, error, staticMode } = useDefenseAsset('ch03/poisson_prefix')
const count = computed(() => payload.value?.T.values.length || 64)
const { index, playing, toggle, seek, reset } = usePlayback(count, 0, 130)
const current = computed(() => {
  if (!payload.value) return new Float32Array()
  const n = payload.value.reference.values.length
  return payload.value.frames.values.subarray(index.value*n, (index.value+1)*n)
})
const difference = computed(() => payload.value
  ? Float32Array.from(current.value, (v,i) => v-payload.value.reference.values[i])
  : new Float32Array())
</script>

<template>
  <div class="poisson-prefix">
    <FigureFrame fallback="/fallback_figures/ch03/poisson_prefix.png" :ready="!!payload" :error="error" :static-mode="staticMode" caption="Fixed scales: solution 0–0.32; error ±0.03 (early errors saturate). Fixed weights and thresholds; T counts spike steps.">
      <div class="poisson-prefix-fields">
        <div>
          <GridField :values="payload.reference.values" :rows="payload.reference.shape[0]" :cols="payload.reference.shape[1]" :center="(payload.field_min+payload.field_max)/2" :limit="(payload.field_max-payload.field_min)/2" palette="jet" title="ANN reference" />
          <p class="field-axis">horizontal: x · vertical: y</p>
        </div>
        <div>
          <GridField :values="current" :rows="payload.reference.shape[0]" :cols="payload.reference.shape[1]" :center="(payload.field_min+payload.field_max)/2" :limit="(payload.field_max-payload.field_min)/2" palette="jet" :title="'SNN · T = '+payload.T.values[index]" />
          <p class="field-axis">horizontal: x · vertical: y</p>
        </div>
        <div>
          <GridField :values="difference" :rows="payload.reference.shape[0]" :cols="payload.reference.shape[1]" :limit="payload.difference_limit" palette="jet" title="Difference · SNN − ANN" />
          <p class="field-axis">horizontal: x · vertical: y</p>
        </div>
      </div>
      <div class="poisson-prefix-readout">
        <span>Relative L₂ vs ANN: <strong>{{ payload.relative_error.values[index].toFixed(4) }}</strong></span>
        <span>One calibration at T = 64 · fixed weights and thresholds</span>
      </div>
      <div class="plot-controls">
        <button @click="toggle">{{ playing ? 'Pause' : 'Play' }}</button>
        <button @click="reset">Reset</button>
        <label for="poisson-prefix-t">T</label>
        <input id="poisson-prefix-t" class="playback-slider" :style="{'--progress': `${100*index/Math.max(1,count-1)}%`}" aria-label="Poisson SNN T" type="range" min="0" :max="count-1" :value="index" @input="seek(Number(($event.target as HTMLInputElement).value))">
        <output>{{ index+1 }} / {{ count }}</output>
        <button v-for="t in [1,16,32,64]" :key="t" :aria-pressed="index === t-1" @click="seek(t-1)">T={{ t }}</button>
      </div>
    </FigureFrame>
    <div class="poisson-prefix-setup">
      <strong>Setup:</strong> <InlineMath tex="-\Delta u=1,\quad (x,y)\in[-1,1]^2,\qquad u|_{\partial\Omega}=0." />
    </div>
  </div>
</template>

<style scoped>
.poisson-prefix :deep(.interactive-figure){height:auto}
.poisson-prefix-fields{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:24px;margin-top:22px}
.poisson-prefix :deep(.field-label){font-size:16px}
.poisson-prefix :deep(.grid-field canvas){width:100%;height:236px;object-fit:contain;margin:10px 0 7px}
.poisson-prefix :deep(.field-scale){font-size:12px}
.poisson-prefix :deep(.field-scale i){width:150px;height:7px}
.poisson-prefix .field-axis{font-size:12px;color:var(--muted);text-align:center;margin:7px 0 0}
.poisson-prefix-readout{display:flex;justify-content:space-between;gap:20px;font-size:14px;margin:17px 0 12px}
.plot-controls{font-size:14px}
.poisson-prefix :deep(.interaction-note){font-size:12px;margin-top:8px}
.poisson-prefix-setup{font-size:14px;display:flex;align-items:baseline;gap:10px;border-top:1px solid var(--line);padding-top:12px;margin-top:18px}
</style>
