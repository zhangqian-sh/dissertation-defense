<script setup lang="ts">
import { ref } from 'vue'
import { useSvgAxisText } from '../composables/useSvgAxisText'
const root = ref<SVGSVGElement>()
useSvgAxisText(root, 12)
// Matched 400k-update runs; checkpoints selected by lowest logged training error.
const results = [
  {name:'BP',sg:{mean:.0204897951,std:.0063863997},wsg:{mean:.0211343057,std:.0064200633}},
  {name:'Global',sg:{mean:.0782655701,std:.0311860982},wsg:{mean:.0842582956,std:.0357180797}},
  {name:'Layerwise',sg:{mean:.0744939074,std:.0315359570},wsg:{mean:.0751678199,std:.0344492272}},
]
const series = [{key:'sg' as const,label:'SG',color:'#7895a6'}, {key:'wsg' as const,label:'WSG',color:'#8b242d'}]
const y=(value:number)=>140-value/.14*115
const x=(i:number)=>126+i*151
const barX=(i:number,key:string)=>x(i)+(key==='sg'?-20:20)
</script>
<template>
<svg ref="root" class="darcy-error-bars" viewBox="0 0 530 180" role="img" aria-label="Darcy test relative L2 mean and standard deviation for matched SG and WSG runs using BP, global and layerwise gradients; checkpoints selected by training error">
  <g v-for="(s,i) in series" :key="s.key">
    <rect :x="348+i*86" y="3" width="12" height="10" :fill="s.color"/>
    <text :x="366+i*86" y="13">{{s.label}}</text>
  </g>
  <g v-for="tick in [0,.02,.04,.06,.08,.1,.12,.14]" :key="tick">
    <path :d="`M49 ${y(tick)} H516`" stroke="#e5e7e5" stroke-width="1"/>
    <text x="42" :y="y(tick)+4" text-anchor="end">{{tick.toFixed(2)}}</text>
  </g>
  <path d="M49 25 V140 H516" stroke="#596361" stroke-width="1.2" fill="none"/>
  <text transform="translate(13 82.5) rotate(-90)" text-anchor="middle">Relative L₂ error</text>
  <g v-for="(item,i) in results" :key="item.name">
    <template v-for="s in series" :key="s.key">
      <g v-if="item[s.key]">
        <rect :x="barX(i,s.key)-14" :y="y(item[s.key]!.mean)" width="28" :height="140-y(item[s.key]!.mean)" :fill="s.color"/>
        <path :d="`M${barX(i,s.key)} ${y(item[s.key]!.mean+item[s.key]!.std)} V${y(item[s.key]!.mean-item[s.key]!.std)} M${barX(i,s.key)-6} ${y(item[s.key]!.mean+item[s.key]!.std)} h12 M${barX(i,s.key)-6} ${y(item[s.key]!.mean-item[s.key]!.std)} h12`" fill="none" stroke="#232727" stroke-width="1.3"/>
        <text :x="barX(i,s.key)" :y="y(item[s.key]!.mean+item[s.key]!.std)-7" text-anchor="middle">{{item[s.key]!.mean.toFixed(3)}}</text>
      </g>
    </template>
    <text :x="x(i)" y="160" text-anchor="middle">{{item.name}}</text>
  </g>
</svg>
</template>
<style scoped>
.darcy-error-bars{display:block;width:100%;height:160px}.darcy-error-bars text{font-family:'Noto Serif',serif;font-size:var(--axis-text-size,12px);fill:#596361}
</style>
