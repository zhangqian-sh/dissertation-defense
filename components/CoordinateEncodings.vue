<script setup lang="ts">
import { ref } from 'vue'
import { useSvgAxisText } from '../composables/useSvgAxisText'
const container=ref<HTMLElement>()
useSvgAxisText(container,12,'svg.encoding-raster')
const size = 8
// Fixed Bernoulli realization for a schematic normalized coordinate grid.
let seed = 17
const rate = Array.from({length:size}, (_, k) => Array.from({length:size}, (_, j) => {
  seed = (1664525 * seed + 1013904223) >>> 0
  return seed / 4294967296 < j / (size - 1)
}))
const methods = [
  {name:'Rate', description:'Probabilistic spikes', cells:rate},
  {name:'Direct', description:'Learned spiking encoder', cells:[]},
  {name:'Ours', description:'Prefix of spikes', cells:Array.from({length:size}, (_, k) => Array.from({length:size}, (_, j) => k <= j))},
]
</script>
<template>
  <div ref="container" class="coordinate-encodings">
    <figure v-for="method in methods" :key="method.name">
      <figcaption>{{method.name}}</figcaption>
      <svg v-if="method.name==='Direct'" viewBox="0 0 200 186" role="img" aria-label="Direct encoding: coordinate input, learned dense projection, spiking dynamics, and averaged readout">
        <defs><marker id="direct-encoder-head" viewBox="0 0 6 6" refX="6" refY="3" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0 L6 3 L0 6 Z" fill="#596361" /></marker></defs>
        <text x="100" y="16" text-anchor="middle">Coordinate input</text>
        <rect x="8" y="26" width="184" height="36" fill="#eeedeb" /><text x="100" y="49" text-anchor="middle">Learned dense layer</text>
        <path d="M100 62 V79" stroke="#596361" marker-end="url(#direct-encoder-head)" />
        <rect x="8" y="79" width="184" height="36" fill="#e7edf1" /><text x="100" y="102" text-anchor="middle">Spiking dynamics</text>
        <path d="M100 115 V132" stroke="#596361" marker-end="url(#direct-encoder-head)" />
        <rect x="8" y="132" width="184" height="36" fill="#eeedeb" /><text x="100" y="155" text-anchor="middle">Averaged readout</text>
      </svg>
      <svg v-else class="encoding-raster" viewBox="0 0 120 132" role="img" :aria-label="method.name + ': ' + method.description">
        <g v-for="(row,k) in method.cells" :key="k">
          <rect v-for="(active,j) in row" :key="j" :x="25+j*10" :y="88-k*10" width="9" height="9" :fill="active?'#315d79':'#eeedeb'" />
        </g>
        <path d="M23 18 V100 H106" fill="none" stroke="#596361" stroke-width=".7" />
        <text x="16" y="96" text-anchor="end">1</text><text x="16" y="26" text-anchor="end">8</text>
        <text x="25" y="112">0</text><text x="105" y="112" text-anchor="end">1</text>
        <text class="axis-label" x="65" y="123" text-anchor="middle">Coordinate</text>
        <text class="axis-label" x="8" y="58" text-anchor="middle" transform="rotate(-90 8 58)">Spike step</text>
      </svg>
    </figure>
  </div>
</template>
<style scoped>
.coordinate-encodings{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}
figure{margin:0;min-width:0}figcaption{text-align:center;font-size:16px;font-weight:600;margin-bottom:4px}
svg{display:block;width:100%;max-height:155px}svg text{font-family:'Noto Serif',serif;font-size:16px;fill:#596361}
svg.encoding-raster text{font-size:12px}
svg.encoding-raster .axis-label{font-size:var(--axis-text-size,12px)}
p{text-align:center;font-size:11px;line-height:1.35;margin:5px 0 0!important}
</style>
