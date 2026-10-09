<script setup lang="ts">
import { computed, ref } from 'vue'
import { useSvgAxisText } from '../composables/useSvgAxisText'
const props=withDefaults(defineProps<{x:ArrayLike<number>;series:Array<{name:string;color:string;y:ArrayLike<number>}>;width?:number;height?:number;cursor?:number;boundary?:number;xLabel?:string;yLabel?:string;minY?:number;maxY?:number;verticalYLabel?:boolean;axisTextSize?:number}>(),{width:350,height:235})
const svgElement=ref<SVGSVGElement>()
if(props.axisTextSize)useSvgAxisText(svgElement,props.axisTextSize)
const emit=defineEmits<{seek:[index:number]}>()
const left=computed(()=>props.verticalYLabel?64:44)
const right=12,bottom=35
const top=computed(()=>props.boundary===undefined?20:32)
const low=computed(()=>props.minY??Math.min(0,...props.series.flatMap(s=>Array.from(s.y))))
const high=computed(()=>props.maxY??Math.max(1e-8,...props.series.flatMap(s=>Array.from(s.y)))*1.06)
const sx=(v:number)=>left.value+(v-props.x[0])/(props.x[props.x.length-1]-props.x[0]||1)*(props.width-left.value-right)
const sy=(v:number)=>top.value+(high.value-v)/(high.value-low.value||1)*(props.height-top.value-bottom)
const path=(y:ArrayLike<number>)=>Array.from(y,(v,i)=>(i?'L':'M')+sx(props.x[i]).toFixed(2)+','+sy(v).toFixed(2)).join(' ')
const tick=(v:number)=>(Math.abs(v)<.001 && v!==0)||Math.abs(v)>=1e4?v.toExponential(1):Number(v.toPrecision(3)).toString()
function seek(event:MouseEvent){const bounds=(event.currentTarget as SVGElement).getBoundingClientRect();const px=(event.clientX-bounds.left)/bounds.width*props.width;const v=props.x[0]+(px-left.value)/(props.width-left.value-right)*(props.x[props.x.length-1]-props.x[0]);let best=0;for(let i=1;i<props.x.length;i++)if(Math.abs(props.x[i]-v)<Math.abs(props.x[best]-v))best=i;emit('seek',best)}
</script>
<template>
  <svg ref="svgElement" class="trace-svg" :viewBox="`0 0 ${width} ${height}`" role="img" :aria-label="`${yLabel} versus ${xLabel}`" @click="seek">
    <g v-for="f in [0,.5,1]" :key="f"><line :x1="left" :x2="width-right" :y1="sy(low+f*(high-low))" :y2="sy(low+f*(high-low))" stroke="#e1e5e3"/><text :x="left-6" :y="sy(low+f*(high-low))+3" text-anchor="end">{{ tick(low+f*(high-low)) }}</text><text :x="sx(x[0]+f*(x[x.length-1]-x[0]))" :y="height-bottom+16" :text-anchor="f===0?'start':f===1?'end':'middle'">{{ tick(x[0]+f*(x[x.length-1]-x[0])) }}</text></g>
    <path v-for="s in series" :key="s.name" :d="path(s.y)" fill="none" :stroke="s.color" stroke-width="1.8"/>
    <template v-if="boundary!==undefined"><line :x1="sx(boundary)" :x2="sx(boundary)" :y1="top" :y2="height-bottom" stroke="#596361" stroke-dasharray="3 3"/><text class="trace-annotation" :x="sx(boundary)+(sx(boundary)<width/2?6:-6)" :y="top-6" :text-anchor="sx(boundary)<width/2?'start':'end'">training end</text></template>
    <line v-if="cursor!==undefined" :x1="sx(x[cursor])" :x2="sx(x[cursor])" :y1="top" :y2="height-bottom" stroke="var(--red)" stroke-width="1.2" stroke-dasharray="3 2"/>
    <text :style="axisTextSize?{fontSize:'var(--axis-text-size,12px)'}:undefined" :x="(width+left-right)/2" :y="height-5" text-anchor="middle">{{xLabel}}</text><text :style="axisTextSize?{fontSize:'var(--axis-text-size,12px)'}:undefined" :x="verticalYLabel?14:3" :y="verticalYLabel?(top+height-bottom)/2:14" :transform="verticalYLabel?`rotate(-90 14 ${(top+height-bottom)/2})`:undefined" :text-anchor="verticalYLabel?'middle':undefined">{{yLabel}}</text>
  </svg>
</template>
