<script setup lang="ts">
import {computed,onMounted,onBeforeUnmount,ref,watch} from 'vue'
import {useIsSlideActive,useNav} from '@slidev/client'
import {publicAssetUrl} from '../composables/publicAssetUrl.mjs'
import {loadAnimationIndex,loadAnimationFrames} from '../composables/animationBundle.mjs'
import FutureEarthFigure from './FutureEarthFigure.vue'
import FutureHideSeekFigure from './FutureHideSeekFigure.vue'
const props=defineProps<{kind:'sequence'|'learning'|'foundation'|'control'}>()
const active=useIsSlideActive(),nav=useNav(),canvas=ref<HTMLCanvasElement>(),phase=ref(.35)
const staticMode=computed(()=>nav.isPrintMode.value||['static','print'].some(key=>new URLSearchParams(location.search).has(key)))
const title=computed(()=>({sequence:'Animated hybrid SNN v-field, the middle-right panel of the ch8-38 reconstruction',learning:'Overhead luminous compute core on a white board with animated electron trails',foundation:'Scientific globe surrounded by atmospheric and fluid field structures',control:'Autonomous aerial agents follow adaptive trajectories around obstacles'}[props.kind]))
let timer:ReturnType<typeof setInterval>|undefined,observer:ResizeObserver|undefined,reduced=false,disposed=false,computeArtwork:HTMLImageElement|undefined
const artworkReady=ref(false),sequenceReady=ref(false),sequenceFrame=ref(0)
let drawingCanvas:HTMLCanvasElement|undefined
let sequenceImage:HTMLImageElement|undefined,sequenceUrls:string[]=[],releaseSequence:(()=>void)|undefined
// Normalized [left, top, width, height] of axes[1,2] in the original figure.
let sequenceCrop=[.61200207,.37918605,.26700851,.26162791]
async function loadSequence(){
 sequenceImage=new Image();sequenceImage.onload=()=>{if(!disposed){sequenceReady.value=true;draw()}}
 if(staticMode.value){sequenceImage.src=publicAssetUrl('/figures/ch08/spiking-rformer-reconstruction.png');return}
 try{
  const meta=await loadAnimationIndex('hybrid')
  if(meta.frames.length!==20||meta.rows[1]!=='v'||meta.columns[2]!=='Hybrid SNN')throw Error('Invalid hybrid sequence')
  sequenceCrop=meta.panel_bounds?.[1]?.[2]??sequenceCrop
  const loaded=await loadAnimationFrames(meta)
  if(disposed){loaded.dispose();return}
  releaseSequence=loaded.dispose;sequenceUrls=loaded.frames.map((frame:string[])=>frame[0]);sequenceImage.src=sequenceUrls[0]
 }catch(error){if(!disposed)sequenceImage.src=publicAssetUrl('/figures/ch08/spiking-rformer-reconstruction.png')}
}
const palette=['#487b9d','#8b242d','#b48b49','#458b82','#72799b','#ac5d4e','#5792af','#638975']
function heat(v:number,alpha=1){
 const a=Math.min(1,Math.abs(v)),rgb=v>0?[173,58,48]:[51,112,155]
 return `rgba(${rgb.map(c=>Math.round(244+(c-244)*a)).join(',')},${alpha})`
}
function ellipse(ctx:CanvasRenderingContext2D,x:number,y:number,rx:number,ry:number,color:string|CanvasGradient){ctx.fillStyle=color;ctx.beginPath();ctx.ellipse(x,y,rx,ry,0,0,Math.PI*2);ctx.fill()}
function polygon(ctx:CanvasRenderingContext2D,points:number[][],fill:string|CanvasGradient,stroke?:string){ctx.beginPath();points.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.closePath();ctx.fillStyle=fill;ctx.fill();if(stroke){ctx.strokeStyle=stroke;ctx.stroke()}}
function fluid(ctx:CanvasRenderingContext2D){
 if(!sequenceReady.value||!sequenceImage?.complete)return
 const [x,y,w,h]=sequenceCrop,iw=sequenceImage.naturalWidth,ih=sequenceImage.naturalHeight
 const sx=x*iw+1,sy=y*ih+1,sw=w*iw-2,sh=h*ih-2,width=126*sw/sh
 ctx.drawImage(sequenceImage,sx,sy,sw,sh,(520-width)/2,0,width,126)
}
function hardware(ctx:CanvasRenderingContext2D){
 if(!artworkReady.value||!computeArtwork)return
 // Show more board around a smaller core, preserving the artwork's aspect.
 const artHeight=104,artWidth=artHeight*computeArtwork.naturalWidth/computeArtwork.naturalHeight,artX=(520-artWidth)/2,artY=11
 ctx.fillStyle='white';ctx.fillRect(0,0,520,126)
 ctx.drawImage(computeArtwork,artX,artY,artWidth,artHeight)
 const left=artX+artWidth*.384,top=artY+artHeight*.165,bottom=artY+artHeight*.778
 const routes:number[][][]=[]
 for(let i=0;i<7;i++){
  const y=top+8+i*8,lane=y+(i-3)*4,bend=left-13-i%3*5,corner=bend-Math.abs(lane-y)
  const path=[[left-1,y],[bend,y],[corner,lane],[157+i%2*6,lane],[150,lane+(i%2?4:-4)]]
  routes.push(path,path.map(([x,y])=>[520-x,y]))
 }
 for(let i=0;i<7;i++){
  const x=left+8+i*8,spread=(i-3)*5
  routes.push([[x,top-1],[x,top-8],[x+spread,7],[x+spread,2]])
  routes.push([[x,bottom+1],[x,bottom+8],[x+spread,119],[x+spread,124]])
 }
 const point=(path:number[][],distance:number)=>{
  for(let i=1;i<path.length;i++){const [x,y]=path[i-1],[xx,yy]=path[i],length=Math.hypot(xx-x,yy-y);if(distance<=length){const t=length?distance/length:0;return {x:x+(xx-x)*t,y:y+(yy-y)*t}}distance-=length}
  const p=path[path.length-1];return {x:p[0],y:p[1]}
 }
 ctx.lineJoin='round';ctx.lineCap='round'
 for(const [index,path] of routes.entries()){
  ctx.beginPath();path.forEach(([x,y],i)=>i?ctx.lineTo(x,y):ctx.moveTo(x,y));ctx.lineWidth=.65;ctx.strokeStyle='rgba(78,144,170,.50)';ctx.stroke()
  if(index%3===1)continue
  const length=path.slice(1).reduce((sum,p,i)=>sum+Math.hypot(p[0]-path[i][0],p[1]-path[i][1]),0),forward=Math.floor(index/2)%2===0
  const travel=(phase.value*650+index*37)%length,head=forward?travel:length-travel
  for(let step=12;step>=0;step--){
   const d=head+(forward?-1:1)*step*1.6;if(d<0||d>length)continue
   const p=point(path,d),alpha=.85*Math.pow(1-step/13,2)
   ctx.shadowColor='rgba(43,157,196,.35)';ctx.shadowBlur=step===0?4:1
   ellipse(ctx,p.x,p.y,step===0?1:.6,step===0?1:.6,`rgba(35,138,181,${alpha})`)
  }
  ctx.shadowBlur=0
 }
 // Slow, restrained illumination on the glass rim suggests ongoing activity.
 ctx.save();ctx.globalCompositeOperation='screen';ctx.lineWidth=1.1
 ctx.strokeStyle=`rgba(75,190,226,${.05+.10*(1+Math.sin(phase.value*6.28))/2})`;ctx.strokeRect(artX+artWidth*.406,artY+artHeight*.221,artWidth*.185,artHeight*.483);ctx.restore()
}
function draw(){
 const el=canvas.value;if(!el||el.clientWidth<=0||props.kind==='foundation'||props.kind==='control')return
 const ratio=Math.min(devicePixelRatio||1,2),w=el.clientWidth,h=el.clientHeight
 if(!drawingCanvas)drawingCanvas=document.createElement('canvas')
 drawingCanvas.width=520*ratio;drawingCanvas.height=126*ratio
 const scene=drawingCanvas.getContext('2d')!;scene.scale(ratio,ratio)
 ;({sequence:fluid,learning:hardware}[props.kind])(scene)
 // Crop the broad source scenes while preserving their geometry. Field data
 // keeps the complete selected panel; hardware/globe focus on their centers.
 const crops={sequence:[130,0,260,126],learning:[150,0,220,126],foundation:[178,0,164,126],control:[135,0,260,126]}
 const [x,y,cw,ch]=crops[props.kind],scale=Math.min(w/cw,h/ch),dw=cw*scale,dh=ch*scale
 el.width=Math.round(w*ratio);el.height=Math.round(h*ratio)
 const ctx=el.getContext('2d')!;ctx.scale(ratio,ratio)
 ctx.drawImage(drawingCanvas,x*ratio,y*ratio,cw*ratio,ch*ratio,(w-dw)/2,(h-dh)/2,dw,dh)
}
function stop(){if(timer)clearInterval(timer);timer=undefined}
function sync(){stop();if(props.kind==='foundation'||props.kind==='control')return;draw();if(active.value&&!staticMode.value&&!document.hidden&&!reduced){const ms=props.kind==='sequence'?250:props.kind==='learning'?40:100;timer=setInterval(()=>{phase.value=props.kind==='learning'?phase.value+.012*ms/100:(phase.value+.012*ms/100)%1;if(props.kind==='sequence'){if(sequenceUrls.length&&sequenceImage){sequenceFrame.value=(sequenceFrame.value+1)%sequenceUrls.length;sequenceImage.src=sequenceUrls[sequenceFrame.value]}}else draw()},ms)}}
watch([active,staticMode],sync)
onMounted(()=>{if(props.kind==='sequence')void loadSequence();if(props.kind==='learning'){computeArtwork=new Image();computeArtwork.onload=()=>{if(!disposed){artworkReady.value=true;draw()}};computeArtwork.src=publicAssetUrl('/figures/ch08/overhead-compute-concept.png')}reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;observer=new ResizeObserver(draw);if(canvas.value)observer.observe(canvas.value);document.addEventListener('visibilitychange',sync);sync()})
onBeforeUnmount(()=>{disposed=true;stop();releaseSequence?.();observer?.disconnect();document.removeEventListener('visibilitychange',sync)})
</script>
<template><FutureEarthFigure v-if="kind==='foundation'" class="future-work-figure foundation" /><FutureHideSeekFigure v-else-if="kind==='control'" class="future-work-figure control" /><canvas v-else ref="canvas" class="future-work-figure" :class="kind" :data-phase="phase" :data-ready="kind==='sequence'?sequenceReady:kind!=='learning'||artworkReady" :data-frame="kind==='sequence'?sequenceFrame:undefined" role="img" :aria-label="title" /></template>
<style scoped>
.future-work-figure{display:block;width:100%;height:126px;margin-top:0}
</style>
