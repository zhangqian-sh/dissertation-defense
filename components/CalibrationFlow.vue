<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, useId } from 'vue'
import katex from 'katex'
const math = (tex: string) => katex.renderToString(tex, { throwOnError: true })
const stage = ref(0)
const busy = ref(false)
const transferring = ref(false)
const calibrated = ref(0)
const calibratedLabels = ref(0)
const outlinedLayers = ref(0)
const annOutputLayers = ref(0)
const snnOutputLayers = ref(0)
const forwardHeads = ref(0)
const targetHeads = ref(0)
const converted = ref(false)
const id = 'calibration-' + useId().replace(/[^a-zA-Z0-9_-]/g, '')
const gradient = ref<SVGLinearGradientElement>()
let animationFrame = 0
onMounted(() => {
  const start = performance.now()
  const flow = (now: number) => {
    // Move the color field in both axes, including vertical targets and arrowheads.
    const shift = ((now - start) % 2400) / 2400 * 180
    gradient.value?.setAttribute('gradientTransform', `translate(${shift} ${shift})`)
    animationFrame = requestAnimationFrame(flow)
  }
  animationFrame = requestAnimationFrame(flow)
})
const layers = [180, 480, 780]
const labels = ['Ready', 'ANN training', 'Conversion directly', 'Calibrate layer 1', 'Calibrate layer 2', 'Calibrate layer 3']
const status = computed(() => stage.value === 5 && !busy.value ? 'Calibration complete' : labels[stage.value])
const nextLabel = computed(() => stage.value < 5 ? labels[stage.value + 1] : 'Complete')
let timers: ReturnType<typeof setTimeout>[] = []
function schedule(fn: () => void, delay: number) { timers.push(setTimeout(fn, delay)) }
// Scale the complete 5500 ms layerwise sequence to exactly 10000 ms.
const calibrationSpeedScale = 10000 / 5500
function scheduleCalibration(fn: () => void, delay: number) { schedule(fn, delay * calibrationSpeedScale) }
function reset() {
  timers.forEach(clearTimeout); timers = []
  stage.value = 0; busy.value = false; transferring.value = false; calibrated.value = 0; calibratedLabels.value = 0; outlinedLayers.value = 0; annOutputLayers.value = 0; snnOutputLayers.value = 0; forwardHeads.value = 0; targetHeads.value = 0; converted.value = false
}
function next() {
  if (busy.value || stage.value === 5) return
  stage.value++; busy.value = true
  if (stage.value < 3) {
    if (stage.value === 2) schedule(() => { converted.value = true }, 1250)
    schedule(() => { busy.value = false }, 1400)
    return
  }
  // The two forward traces arrive together, then the ANN target crosses downward.
  transferring.value = false
  // Forward trace: 900 ms. Only then trace the new block's perimeter (1200 ms).
  scheduleCalibration(() => { outlinedLayers.value = stage.value - 2 }, 950)
  // Trace the ANN outlet to its branch before sending the target downward.
  scheduleCalibration(() => { annOutputLayers.value = stage.value - 2 }, 2200)
  scheduleCalibration(() => { transferring.value = true }, 2700)
  // Once the ANN target reaches the difference node, trace the SNN outlet.
  scheduleCalibration(() => { snnOutputLayers.value = stage.value - 2 }, 3650)
  // Both inputs have arrived: now calibrate, then finish the green transition.
  scheduleCalibration(() => { calibrated.value = stage.value - 2 }, 4150)
  scheduleCalibration(() => { calibratedLabels.value = stage.value - 2; busy.value = false }, 5500)
}
onBeforeUnmount(() => { timers.forEach(clearTimeout); cancelAnimationFrame(animationFrame) })
const activeLayers = computed(() => Math.max(0, stage.value - 2))
function segment(i: number, y: number) {
  const start = i === 0 ? 88 : layers[i - 1] + 140
  const end = i < 3 ? layers[i] - 8 : 1036
  return `M${start} ${y} H${end}`
}
</script>

<template>
<section class="calibration-animation" :style="{
  '--forward-duration': `${900 * calibrationSpeedScale}ms`,
  '--perimeter-duration': `${1200 * calibrationSpeedScale}ms`,
  '--outlet-duration': `${450 * calibrationSpeedScale}ms`,
  '--calibration-duration': `${1250 * calibrationSpeedScale}ms`
}" @click.stop @pointerdown.stop @keydown.stop aria-label="Interactive ANN conversion and layerwise calibration">
  <div class="calibration-controls">
    <div class="stage-status" aria-live="polite"><strong>{{ status }}</strong><span>{{ stage }} / 5</span></div>
    <button type="button" @click="reset">Reset</button>
    <button type="button" :disabled="busy || stage === 5" @click="next">Next<span v-if="stage < 5"> · {{ nextLabel }}</span></button>
  </div>
  <div class="calibration-scene" :class="{ trained: stage >= 1, converted: converted, converting: stage === 2 && busy }">
    <svg class="flow-geometry" viewBox="0 0 1088 370" aria-hidden="true">
      <defs>
        <linearGradient ref="gradient" :id="id" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="180" y2="180" spreadMethod="repeat">
          <stop offset="0" stop-color="#bb4675"/><stop offset=".2" stop-color="#cd8a3b"/><stop offset=".4" stop-color="#699a45"/><stop offset=".6" stop-color="#369aab"/><stop offset=".8" stop-color="#7168bc"/><stop offset="1" stop-color="#bb4675"/>
        </linearGradient>
      </defs>
      <g v-for="y in (converted ? [92, 284] : [92])" :key="y">
        <g v-for="i in 4" :key="i">
          <path :d="segment(i - 1, y)" class="base-line"/>
          <polygon :points="`${i < 4 ? layers[i - 1] : 1044},${y} ${i < 4 ? layers[i - 1] - 8 : 1036},${y - 4} ${i < 4 ? layers[i - 1] - 8 : 1036},${y + 4}`" :style="{ fill: forwardHeads >= i ? `url(#${id})` : undefined }" class="arrow-head"/>
          <path v-if="activeLayers >= i || (stage === 5 && !busy)" :key="'flow'+i" :d="segment(i - 1, y)" class="forward-flow" :stroke="`url(#${id})`" pathLength="1" @animationend="forwardHeads = Math.max(forwardHeads, i)"/>
        </g>
        <template v-for="(x, i) in layers" :key="'perimeter'+i">
          <path v-if="outlinedLayers > i" :d="`M${x} ${y} v-44 h140 v88 h-140 v-44`" class="flow-perimeter" :stroke="`url(#${id})`" pathLength="1"/>
        </template>
      </g>
      <g v-for="(x, i) in layers" :key="'target'+i">
        <!-- Trace both output segments explicitly before changing the SNN parameters. -->
        <path v-if="annOutputLayers > i" :d="`M${x + 140} 92 H${x + 176}`" class="outlet-flow ann-outlet" :stroke="`url(#${id})`" pathLength="1"/>
        <path v-if="snnOutputLayers > i" :d="`M${x + 140} 284 H${x + 163}`" class="outlet-flow snn-outlet" :stroke="`url(#${id})`" pathLength="1"/>
        <path v-if="activeLayers > i && (activeLayers > i + 1 || transferring)" :d="`M${x + 176} 92 V265`" class="target-flow" :stroke="`url(#${id})`" pathLength="1" @animationend="targetHeads = Math.max(targetHeads, i + 1)"/>
        <polygon v-if="targetHeads > i" :points="`${x + 176},271 ${x + 172},263 ${x + 180},263`" :style="{ fill: `url(#${id})` }" class="arrow-head"/>
        <circle v-if="activeLayers > i" :cx="x + 176" cy="284" r="13" class="comparison-circle"/>
        <path v-if="activeLayers > i" :d="`M${x + 171} 284 h10`" class="base-line"/>
      </g>
    </svg>
    <strong class="row-name ann-name">ANN</strong><strong v-if="converted" class="row-name snn-name">SNN</strong>
    <span class="input-label ann-input" v-html="math('x')"/><span v-if="converted" class="input-label snn-input" v-html="math('x')"/>
    <span class="output-label ann-output" v-html="math(String.raw`x_3`)"/><span v-if="converted" class="output-label snn-output" v-html="math(String.raw`\bar s_3`)"/>
    <template v-for="(x, i) in layers" :key="i">
      <div class="layer-block ann-block" :style="{ left: x / 10.88 + '%' }">
        <strong>ANN layer {{ i + 1 }}</strong><span v-html="math(String.raw`W_${i + 1},\,b_${i + 1}\;\to\;f`)"/>
      </div>
      <div v-if="converted" class="layer-block snn-block" :class="{ calibrated: calibrated > i }" :style="{ left: x / 10.88 + '%' }">
        <strong>SNN layer {{ i + 1 }}</strong><span v-html="math(calibratedLabels > i ? String.raw`\widetilde W_${i + 1},\,\widetilde b_${i + 1}\;\to\;\mathrm{IF}` : String.raw`W_${i + 1},\,b_${i + 1}\;\to\;\mathrm{IF}`)"/>
      </div>
      <span v-if="activeLayers > i && (activeLayers > i + 1 || transferring)" class="target-label" :style="{ left: (x + 184) / 10.88 + '%' }" v-html="math(String.raw`x_${i + 1}`)"/>
      <span v-if="activeLayers > i" class="mismatch-label" :style="{ left: (x + 176) / 10.88 + '%' }" v-html="math(String.raw`\|x_${i + 1}-\bar s_${i + 1}\|_2^2`)"/>
    </template>
    <!-- Move an entire ANN copy; only its landed row becomes the SNN. -->
    <div v-if="stage === 2 && !converted" class="conversion-copy" aria-hidden="true">
      <svg class="copy-geometry" viewBox="0 0 1088 370">
        <g v-for="i in 4" :key="i">
          <path :d="segment(i - 1, 92)" class="base-line"/>
          <polygon :points="`${i < 4 ? layers[i - 1] : 1044},92 ${i < 4 ? layers[i - 1] - 8 : 1036},88 ${i < 4 ? layers[i - 1] - 8 : 1036},96`" class="arrow-head"/>
        </g>
      </svg>
      <strong class="row-name ann-name">ANN</strong>
      <span class="input-label ann-input" v-html="math('x')"/>
      <span class="output-label ann-output" v-html="math(String.raw`x_3`)"/>
      <div v-for="(x, i) in layers" :key="i" class="layer-block ann-block" :style="{ left: x / 10.88 + '%' }">
        <strong>ANN layer {{ i + 1 }}</strong><span v-html="math(String.raw`W_${i + 1},\,b_${i + 1}\;\to\;f`)"/>
      </div>
    </div>
  </div>
  <div class="calibration-key"><span><i class="red-key"/>Trained / copied parameters</span><span><i class="green-key"/>Calibrated parameters</span><span class="spike-average" v-html="math(String.raw`\bar s_l=\frac{1}{T}\sum_{k=1}^{T}s_l[k]`)"/></div>
  <p class="calibration-explanation">ANN outputs supply fixed targets. Calibrate one SNN layer at a time using outputs from previously calibrated layers.</p>
</section>
</template>

<style scoped>
.calibration-animation{font-size:14px}.calibration-controls{display:flex;align-items:center;gap:10px;margin-bottom:12px;height:36px}.stage-status{display:flex;align-items:center;gap:16px;flex:1}.stage-status strong{font-size:16px}.stage-status span{color:#596361}.calibration-controls button{font:inherit;background:white;color:#232727;border:1px solid #98a4ae;padding:6px 12px;border-radius:2px;cursor:pointer}.calibration-controls button:disabled{opacity:.45;cursor:default}.calibration-controls button:focus-visible{outline:2px solid #4e3629;outline-offset:3px}
.calibration-scene{position:relative;height:370px;width:100%}.flow-geometry{position:absolute;inset:0;width:100%;height:370px;z-index:1;pointer-events:none}.base-line{fill:none;stroke:#596361;stroke-width:1.6;stroke-linecap:butt}.arrow-head{fill:#596361}.outlet-flow{fill:none;stroke-width:3;stroke-dasharray:1;stroke-dashoffset:0;animation:forward-arrival var(--outlet-duration) linear both}.forward-flow,.target-flow{fill:none;stroke-width:3;stroke-dasharray:1;stroke-dashoffset:0;animation:forward-arrival var(--forward-duration) linear both}.target-base{fill:none;stroke:#b9bfbd;stroke-width:1.2}.flow-perimeter{fill:none;stroke-width:2.5;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:0;animation:perimeter-arrival var(--perimeter-duration) linear both;filter:drop-shadow(0 0 2px #718da855)}.comparison-circle{fill:white;stroke:#596361;stroke-width:1.4}
.layer-block{position:absolute;width:12.868%;height:88px;display:flex;flex-direction:column;justify-content:center;align-items:center;gap:9px;border:1px solid #98a4ae;border-radius:2px;background:#f5f5f4;font-size:16px;transition:background-color 1.25s ease,border-color 1.25s ease}.layer-block strong{font-size:16px;font-weight:600}.ann-block{top:48px}.snn-block{top:240px;background:white}.trained .ann-block,.converted .snn-block{background:#f4d7d4;border-color:#b34f49}.converted .snn-block{transition:none}.converted .snn-block.calibrated{transition:background-color var(--calibration-duration) ease,border-color var(--calibration-duration) ease;background:#d6e8d8;border-color:#538761}.conversion-copy{position:absolute;inset:0;z-index:3;pointer-events:none;animation:copy-down 1.25s ease-in-out forwards}.copy-geometry{position:absolute;inset:0;width:100%;height:370px}.row-name{position:absolute;left:0;font-size:16px}.ann-name{top:16px}.snn-name{top:208px}.input-label,.output-label{position:absolute;font-size:16px;transform:translateY(-50%)}.input-label{left:4%}.output-label{left:96.3%}.ann-input,.ann-output{top:92px}.snn-input,.snn-output{top:284px}.target-label{position:absolute;top:175px;font-size:16px;animation:target-label-appear var(--forward-duration) ease both}.mismatch-label{position:absolute;top:334px;transform:translateX(-50%);font-size:14px}.calibration-key{display:flex;align-items:center;gap:26px;margin-top:8px;font-size:14px}.calibration-key>span{display:flex;align-items:center;gap:8px}.calibration-key i{display:inline-block;width:12px;height:12px;border:1px solid #98a4ae}.red-key{background:#f4d7d4}.green-key{background:#d6e8d8}.spike-average{margin-left:auto;font-size:16px}.calibration-explanation{font-size:14px;color:#596361;margin:12px 0 0;line-height:1.45}
@keyframes target-label-appear{from{opacity:0}to{opacity:1}}
@keyframes perimeter-arrival{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}
@keyframes forward-arrival{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}@keyframes copy-down{from{transform:translateY(0);opacity:1}to{transform:translateY(192px);opacity:1}}
</style>
