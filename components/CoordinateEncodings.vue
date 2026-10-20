<script setup lang="ts">
import { ref } from 'vue'
import InlineMath from './InlineMath.vue'
const props=withDefaults(defineProps<{layout?:'row'|'column'}>(),{layout:'row'})
import { useSvgAxisText } from '../composables/useSvgAxisText'
const container=ref<HTMLElement>()
useSvgAxisText(container,12,'svg.encoding-raster')
useSvgAxisText(container,16,'svg.direct-compact')
const size = 8
const coordinateSamples = 9
// Fixed Bernoulli realization for a schematic normalized coordinate grid.
let seed = 17
const rate = Array.from({length:size}, (_, k) => Array.from({length:coordinateSamples}, (_, j) => {
  seed = (1664525 * seed + 1013904223) >>> 0
  return seed / 4294967296 < j / (coordinateSamples - 1)
}))
const methods = [
  {name:'Rate', description:'Probabilistic spikes', cells:rate},
  {name:'Direct', description:'Learned spiking encoder', cells:[]},
  {name:'Ours', description:'Prefix of spikes', cells:Array.from({length:size}, (_, k) => Array.from({length:coordinateSamples}, (_, j) => k < Math.floor(size*j/(coordinateSamples-1))))},
]
</script>
<template>
  <div ref="container" class="coordinate-encodings" :class="props.layout">
    <figure v-for="method in methods" :key="method.name" :class="{'method-direct':method.name==='Direct'}">
      <figcaption class="method-identity"><span class="method-name">{{method.name}}</span>
      <div v-if="props.layout==='column' && method.name!=='Direct'" class="method-formula"><InlineMath :tex="method.name==='Rate'?'\\Pr(s[k]=1)=a':'N=\\lfloor Ka\\rfloor'" /></div></figcaption>
      <svg v-if="method.name==='Direct' && props.layout==='column'" class="direct-compact" viewBox="0 0 360 100" role="img" aria-label="Direct encoding: input passes through a learned dense layer, spiking dynamics, and mean readout">
        <g v-for="(label,i) in [['Input'],['Learned','dense'],['Spiking','dynamics'],['Mean','readout']]" :key="i">
          <rect :x="i*96" y="25" width="72" height="58" fill="#f1efed" />
          <text v-for="(line,j) in label" :key="j" :x="i*96+36" :y="label.length===1?60:48+j*22" text-anchor="middle">{{line}}</text>
          <path v-if="i<3" :d="`M${i*96+72} 54 H${i*96+90}`" fill="none" stroke="#596361" stroke-width="1.4" />
          <polygon v-if="i<3" :points="`${i*96+96},54 ${i*96+88},50.5 ${i*96+88},57.5`" fill="#596361" />
        </g>
      </svg>
      <svg v-else-if="method.name==='Direct'" viewBox="0 0 200 186" role="img" aria-label="Direct encoding: coordinate input, learned dense projection, spiking dynamics, and averaged readout">
        <defs><marker id="direct-encoder-head" viewBox="0 0 6 6" refX="6" refY="3" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L6 3 L0 6 Z" fill="#596361" /></marker></defs>
        <text x="100" y="16" text-anchor="middle">Coordinate input</text>
        <rect x="8" y="26" width="184" height="36" fill="#eeedeb" /><text x="100" y="49" text-anchor="middle">Learned dense layer</text>
        <path d="M100 62 V79" stroke="#596361" marker-end="url(#direct-encoder-head)" />
        <rect x="8" y="79" width="184" height="36" fill="#eeeae7" /><text x="100" y="102" text-anchor="middle">Spiking dynamics</text>
        <path d="M100 115 V132" stroke="#596361" marker-end="url(#direct-encoder-head)" />
        <rect x="8" y="132" width="184" height="36" fill="#eeedeb" /><text x="100" y="155" text-anchor="middle">Averaged readout</text>
      </svg>
      <svg v-else class="encoding-raster" viewBox="0 0 130 132" role="img" :aria-label="method.name + ': ' + method.description">
        <g v-for="(row,k) in method.cells" :key="k">
          <rect v-for="(active,j) in row" :key="j" :x="25+j*10" :y="88-k*10" width="9" height="9" :fill="active?'#4e3629':'#eeedeb'" />
        </g>
        <path d="M23 18 V100 H116" fill="none" stroke="#596361" stroke-width=".7" />
        <text x="16" y="96" text-anchor="end">1</text><text x="16" y="26" text-anchor="end">8</text>
        <text x="25" y="112">0</text><text x="115" y="112" text-anchor="end">1</text>
        <text class="axis-label" x="70" y="123" text-anchor="middle">Coordinate</text>
        <text class="axis-label" x="8" y="58" text-anchor="middle" transform="rotate(-90 8 58)">Spike step</text>
      </svg>
    </figure>
  </div>
</template>
<style scoped>
.coordinate-encodings{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
figure{margin:0;min-width:0}figcaption{text-align:center;font-size:16px;font-weight:600;margin-bottom:4px}
svg{display:block;width:100%;max-height:155px}svg text{font-family:'Noto Serif',serif;font-size:16px;fill:#596361}
svg.encoding-raster text{font-size:var(--axis-text-size,12px)}
svg.encoding-raster .axis-label{font-size:var(--axis-text-size,12px)}
.column{display:flex;flex-direction:column;gap:12px}
.column figure{display:grid;grid-template-columns:minmax(0,1fr) 140px;gap:12px;align-items:center}
.column figcaption{text-align:left}
.column svg{height:126px;max-height:126px}
.column .method-formula{font-size:14px;font-weight:400;margin-top:8px}
.column .method-direct{display:block}
.column .direct-compact{height:auto;max-height:100px}
.direct-compact text{font-size:var(--axis-text-size,16px)}
p{text-align:center;font-size:11px;line-height:1.35;margin:5px 0 0!important}
</style>
