<script setup lang="ts">
import {ref,onMounted,watch} from 'vue'
import {scalarColors} from '../composables/fieldRaster.mjs'
const props=withDefaults(defineProps<{values:ArrayLike<number>;rows:number;cols:number;limit:number;center?:number;title:string}>(),{center:0})
const canvas=ref<HTMLCanvasElement>()
function draw(){
 const el=canvas.value;if(!el)return
 const flipped=new Float64Array(props.rows*props.cols)
 for(let r=0;r<props.rows;r++)for(let c=0;c<props.cols;c++)flipped[(props.rows-1-r)*props.cols+c]=props.values[r*props.cols+c]-props.center
 const ctx=el.getContext('2d')!;ctx.imageSmoothingEnabled=false
 ctx.putImageData(new ImageData(scalarColors(flipped,props.limit),props.cols,props.rows),0,0)
}
onMounted(draw);watch(()=>[props.values,props.limit,props.center],draw)
</script>
<template><div class="grid-field"><div class="field-label">{{title}}</div><canvas ref="canvas" :width="cols" :height="rows" role="img" :aria-label="title"/><div class="field-scale"><span>{{(center-limit).toPrecision(2)}}</span><i/><span>{{(center+limit).toPrecision(2)}}</span></div></div></template>
