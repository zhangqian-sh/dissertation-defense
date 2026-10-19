<script setup lang="ts">
import { ref } from 'vue'
import 'katex/dist/katex.min.css'
import InlineMath from './InlineMath.vue'
import { useSvgAxisText } from '../composables/useSvgAxisText'

// An illustrative LIF neuron: weighted impulses, exponential leak, hard reset.
// Sample u before resetting v so threshold crossings remain visible in the trace.
const inputSteps = [3, 7, 8, 20, 21, 22, 36, 40, 41]
const beta = 0.90, weight = 0.60, threshold = 1
const steps = 48
const x = (k: number) => 52 + k / steps * 560
const y = (v: number) => 274 - v * 80
const outputSteps: number[] = []
let voltage = 0
let voltagePath = `M${x(0)},${y(0)}`
for (let k = 1; k <= steps; k++) {
  const decayed = beta * voltage
  voltagePath += ` L${x(k)},${y(decayed)}`
  const potential = decayed + (inputSteps.includes(k) ? weight : 0)
  if (potential !== decayed) voltagePath += ` L${x(k)},${y(potential)}`
  if (potential >= threshold) {
    outputSteps.push(k)
    voltage = 0
    voltagePath += ` L${x(k)},${y(0)}`
  } else voltage = potential
}
const trace = ref<SVGSVGElement>()
useSvgAxisText(trace, 12)
const layers = [[32, 64, 96], [24, 52, 80, 108], [46, 86]]
</script>

<template>
  <div class="snn-intro">
    <section class="snn-explanation">
      <h2>A network of spiking neurons</h2>
      <p>Neurons carry a membrane voltage. They communicate through binary events, or <strong>spikes</strong>, over time.</p>
      <svg class="snn-network" viewBox="0 0 340 132" role="img" aria-label="Three connected layers of stateful spiking neurons. Highlighted neurons and connections illustrate spike transmission.">
        <g v-for="(layer, i) in layers.slice(0, -1)" :key="i">
          <g v-for="(cy, j) in layer" :key="j">
            <line v-for="(nextY, n) in layers[i + 1]" :key="n" :x1="48 + i * 118" :y1="cy" :x2="166 + i * 118" :y2="nextY" :class="{ active: (i === 0 && j === 1 && n === 2) || (i === 1 && j === 2 && n === 0) }" />
          </g>
        </g>
        <g v-for="(layer, i) in layers" :key="i">
          <circle v-for="(cy, j) in layer" :key="j" :cx="48 + i * 118" :cy="cy" r="10" :class="{ active: j === [1, 2, 0][i] }" />
        </g>
      </svg>
      <div class="snn-model">
        <h2>Leaky integrate-and-fire (LIF)</h2>
        <div class="snn-equations">
          <InlineMath tex="u[k]=\beta v[k-1]+\sum_j w_j s_j[k]" />
          <InlineMath tex="s[k]=\mathbf{1}_{u[k]\geq v_{\mathrm{th}}}" />
          <InlineMath tex="v[k]=u[k]\,(1-s[k])" />
        </div>
        <p><InlineMath tex="\beta\in(0,1)" />: voltage retention; <InlineMath tex="w_j" />: synaptic weight;<br><InlineMath tex="v_{\mathrm{th}}" />: firing threshold; <InlineMath tex="k" />: spike step.</p>
      </div>
      <p class="snn-binary">The transmitted signal is binary; the internal voltage is real-valued.</p>
    </section>
    <figure class="snn-timing">
      <h2>From input spikes to output spikes</h2>
      <svg ref="trace" viewBox="0 0 640 388" role="img" :aria-label="`Aligned input spike train, membrane voltage and output spike train. Inputs accumulate with leak; threshold crossings at steps ${outputSteps.join(', ')} produce output spikes and reset the voltage to zero.`">
        <g class="event-guides">
          <path v-for="k in outputSteps" :key="k" :d="`M${x(k)} 56 V350`" />
        </g>
        <g class="axis">
          <path d="M52 58 V100 H612 M52 145 V274 H612 M52 319 V350 H612" />
          <path v-for="k in [0, 12, 24, 36, 48]" :key="k" :d="`M${x(k)} 350 v5`" />
        </g>
        <text class="row-label" x="52" y="34">Input spikes</text>
        <path v-for="k in inputSteps" :key="k" class="spike" :d="`M${x(k)} 100 V66`" />
        <text class="row-label" x="52" y="133">Membrane voltage</text>
        <path class="threshold" :d="`M52 ${y(threshold)} H612`" />
        <text class="threshold-label" :x="x(outputSteps[1]) + 12" :y="y(threshold) - 8">Firing threshold</text>
        <path class="voltage" :d="voltagePath" />
        <circle v-for="k in outputSteps" :key="k" class="reset-dot" :cx="x(k)" :cy="y(0)" r="3.1" />
        <text class="row-label" x="52" y="309">Output spikes</text>
        <path v-for="k in outputSteps" :key="k" class="spike" :d="`M${x(k)} 350 V322`" />
        <text v-for="k in [0, 12, 24, 36, 48]" :key="k" :x="x(k)" y="373" text-anchor="middle">{{ k }}</text>
        <text x="332" y="387" text-anchor="middle">Spike step k</text>
        <text :x="x(inputSteps[5]) + 14" y="224" class="process-label">Leak</text>
        <text :x="x(inputSteps[2]) + 9" y="252" class="process-label">Reset</text>
      </svg>
      <figcaption>Weighted inputs accumulate; the voltage leaks between inputs.<br>Cross the threshold → emit a spike and reset.</figcaption>
    </figure>
  </div>
</template>

<style scoped>
.snn-intro{display:grid;grid-template-columns:0.38fr 0.62fr;gap:36px;align-items:start;margin-top:8px}
.snn-intro h2{font-size:16px;line-height:1.35;margin:0 0 12px;font-weight:600}
.snn-intro p{font-size:14px;line-height:1.55;margin:0 0 12px}
.snn-explanation,.snn-timing{min-width:0}
.snn-network{display:block;width:100%;height:104px;margin:2px 0 13px}
.snn-network line{stroke:#dce1df;stroke-width:1.1}
.snn-network line.active{stroke:var(--brown);stroke-width:2}
.snn-network circle{fill:white;stroke:#98a4ae;stroke-width:1.4}
.snn-network circle.active{fill:var(--brown);stroke:var(--brown)}
.snn-model{border-top:2px solid var(--brown);padding-top:12px}
.snn-equations{display:flex;flex-direction:column;gap:9px;font-size:16px;margin:14px 0}
.snn-model p{color:var(--muted)}
.snn-intro .snn-binary{padding:9px 12px;background:var(--brown-wash);margin-top:14px}
.snn-timing{margin:0;border-left:1px solid var(--line);padding-left:25px}
.snn-timing svg{display:block;width:100%;height:auto;overflow:visible}
.snn-timing svg text{font-family:'Noto Serif',serif;font-size:var(--axis-text-size,12px);fill:var(--muted)}
.snn-timing svg .row-label{font-size:calc(var(--axis-text-size,12px) * 4 / 3);fill:var(--ink)}
.axis path{fill:none;stroke:#98a4ae;stroke-width:1}
.event-guides path{fill:none;stroke:#e1dedb;stroke-width:1;stroke-dasharray:3 5}
.spike{fill:none;stroke:var(--brown);stroke-width:3;stroke-linecap:butt}
.threshold{fill:none;stroke:#98a4ae;stroke-width:1.3;stroke-dasharray:5 4}
.voltage{fill:none;stroke:var(--red);stroke-width:2.2;stroke-linejoin:round}
.reset-dot{fill:var(--red)}
.snn-timing figcaption{font-size:14px;line-height:1.55;margin-top:18px;color:var(--ink)}
</style>
