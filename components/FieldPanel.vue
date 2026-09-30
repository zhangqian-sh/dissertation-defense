<script setup lang="ts">
import {ref,watch,onMounted} from 'vue'
import type {Tensor} from '../composables/useDefenseAsset'
import {meshRaster,interpolateRaster,scalarColors} from '../composables/fieldRaster.mjs'
const props=defineProps<{coordinates:Tensor;cells:Tensor;values:ArrayLike<number>;limit:number;title:string}>()
const canvas=ref<HTMLCanvasElement>()
let raster:ReturnType<typeof meshRaster>,buffer:HTMLCanvasElement
function draw(){
 const el=canvas.value;if(!el)return
 if(!raster){raster=meshRaster(props.coordinates.values,props.cells.values);buffer=document.createElement('canvas');buffer.width=buffer.height=raster.size}
 const pixels=scalarColors(interpolateRaster(raster,props.values),props.limit)
 buffer.getContext('2d')!.putImageData(new ImageData(pixels,raster.size,raster.size),0,0)
 const ctx=el.getContext('2d')!;ctx.clearRect(0,0,320,260);ctx.imageSmoothingEnabled=true;ctx.imageSmoothingQuality='high'
 ctx.drawImage(buffer,35,5,250,250)
}
onMounted(draw);watch(()=>[props.values,props.limit],draw)
</script>
<template><div class="field-panel"><div class="field-label">{{title}}</div><canvas ref="canvas" width="320" height="260" role="img" :aria-label="title"/><div class="field-scale"><span>{{(-limit).toPrecision(2)}}</span><i/><span>{{limit.toPrecision(2)}}</span></div></div></template>
