<script setup lang="ts">
import {computed,onMounted,onBeforeUnmount,ref,watch} from 'vue'
import {useIsSlideActive,useNav} from '@slidev/client'
import {loadAsset} from '../composables/useDefenseAsset'
import {loadAnimationIndex,loadAnimationFrames} from '../composables/animationBundle.mjs'
import {publicAssetUrl} from '../composables/publicAssetUrl.mjs'
import {scalarColors} from '../composables/fieldRaster.mjs'
const props=defineProps<{kind:'encoding'|'conversion'|'training'|'energy'|'reconstruction'|'control'}>()
const active=useIsSlideActive(),nav=useNav(),staticMode=computed(()=>nav.isPrintMode.value||['static','print'].some(k=>new URLSearchParams(location.search).has(k)))
const canvas=ref<HTMLCanvasElement>(),index=ref(0),ready=ref(false),failed=ref(false),urls=ref<string[]>([])
let energyStep=0,timer:ReturnType<typeof setInterval>|undefined,disposed=false,release:(()=>void)|undefined,energy:any,swarm:any,positions:Float32Array
const caption=computed(()=>({encoding:'Function and spike encoding',conversion:'Loihi 2 · 16-bit prediction',training:'Forward-trained Darcy solution',energy:'Energy-guided reconstruction',reconstruction:'RFormer · reconstructed wake',control:'OCFormer · learned trajectories'}[props.kind]))
const field=(x:number)=>.15*Math.exp(-Math.pow((x-.14)/.12,2))+.18*Math.exp(-Math.pow((x-.48)/.16,2))
const curve=Array.from({length:101},(_,i)=>`${20+i*1.66},${36-field(i/100)*165}`).join(' ')
const cells=Array.from({length:51},(_,i)=>Array.from({length:Math.floor(40*field(i/50)/.2)},(_,k)=>({x:20+i*166/51,y:108-(k+1)*1.45}))).flat()
function draw(){
 const el=canvas.value;if(!el||!ready.value)return
 const ctx=el.getContext('2d')!
 if(props.kind==='energy'){
  const [rows,cols]=energy.reference.shape,n=rows*cols,frame=staticMode.value?11:index.value
  el.width=cols;el.height=rows
  const flipped=new Float64Array(n)
  for(let r=0;r<rows;r++)for(let c=0;c<cols;c++)flipped[(rows-1-r)*cols+c]=energy.frames.values[frame*n+r*cols+c]-.5
  ctx.putImageData(new ImageData(scalarColors(flipped,.5),cols,rows),0,0)
 }else if(props.kind==='control'){
  const t=staticMode.value?99:index.value,side=130,ratio=devicePixelRatio||1
  el.width=side*ratio;el.height=side*ratio;ctx.scale(ratio,ratio);ctx.clearRect(0,0,side,side)
  const point=(k:number,a:number,j:number)=>positions[swarm.float_offset+(k*8+a)*2+j]
  const x=(n:number)=>(n+.55)/1.1*side,y=(n:number)=>(.55-n)/1.1*side
  ctx.lineWidth=.7;ctx.strokeStyle='rgba(110,110,110,.3)'
  for(let a=0;a<8;a++){ctx.beginPath();for(let k=0;k<=t;k++){if(!k)ctx.moveTo(x(point(k,a,0)),y(point(k,a,1)));else ctx.lineTo(x(point(k,a,0)),y(point(k,a,1)))}ctx.stroke()}
  ctx.lineWidth=1.3
  for(let a=0;a<8;a++){ctx.strokeStyle=swarm.colors[a];ctx.beginPath();ctx.arc(x(point(t,a,0)),y(point(t,a,1)),swarm.radius/1.1*side,0,2*Math.PI);ctx.stroke()}
 }
}
function stop(){if(timer)clearInterval(timer);timer=undefined}
function start(){
 stop();if(!ready.value||!active.value||staticMode.value||document.hidden)return
 if(!['energy','reconstruction','control'].includes(props.kind))return
 timer=setInterval(()=>{
  const count=props.kind==='reconstruction'?urls.value.length:200
  // Retain the final energy update for three ticks before restarting.
  if(props.kind==='energy'){energyStep=(energyStep+1)%15;index.value=Math.min(energyStep,11)}
  else index.value=(index.value+1)%count
  draw()
 },props.kind==='energy'?650:props.kind==='reconstruction'?250:50)
}
watch([active,ready,staticMode],()=>{start();draw()})
const visibility=()=>start()
onMounted(async()=>{
 document.addEventListener('visibilitychange',visibility)
 try{
  if(props.kind==='energy'){
   const d=await loadAsset('ch05/energy_history');energy=d.data.states[0].payload
   if(energy.frames.shape.join(',')!=='12,128,256')throw Error('Unexpected energy frames')
  }else if(props.kind==='reconstruction'&&!staticMode.value){
   const d=await loadAnimationIndex('vortex'),loaded=await loadAnimationFrames(d)
   if(disposed){loaded.dispose();return}release=loaded.dispose;urls.value=loaded.frames.map(f=>f[0])
  }else if(props.kind==='control'){
   const r=await fetch(publicAssetUrl('/data/ch07/swarm-scaling/index.json'));if(!r.ok)throw Error('Missing swarm index');const m=await r.json();swarm=m.cases.find((c:any)=>c.agents===8)
   const b=await fetch(publicAssetUrl(m.binary.path));if(!b.ok)throw Error('Missing trajectories');const bytes=await b.arrayBuffer()
   const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))).map(v=>v.toString(16).padStart(2,'0')).join('')
   if(hash!==m.binary.sha256||bytes.byteLength!==m.binary.byte_length||swarm.shape.join(',')!=='200,8,2')throw Error('Invalid trajectory data')
   positions=new Float32Array(bytes)
  }
  if(disposed)return;ready.value=true;draw();start()
 }catch{if(!disposed)failed.value=true}
})
onBeforeUnmount(()=>{disposed=true;stop();release?.();document.removeEventListener('visibilitychange',visibility)})
</script>
<template>
<figure class="contribution-figure" :class="kind">
 <svg v-if="kind==='encoding'" class="encoding-mini" viewBox="0 0 190 110" role="img" aria-label="The continuous example function and its magnitude-prefix spike encoding from chapter 2">
  <polyline :points="curve" fill="none" stroke="#315d79" stroke-width="1.6" />
  <line x1="20" y1="38" x2="186" y2="38" stroke="#dce1df" />
  <rect v-for="(cell,i) in cells" :key="i" :x="cell.x" :y="cell.y" width="2.8" height="1.15" fill="#315d79" />
 </svg>
 <svg v-else-if="kind==='conversion'" class="square-mini" viewBox="55 4 306 324" role="img" aria-label="Loihi 2 fixed-point prediction from the conversion experiment">
  <image :href="publicAssetUrl('/figures/ch03/loihi_precision_16bit.png')" width="372" height="350" />
 </svg>
 <svg v-else-if="kind==='training'" class="square-mini" viewBox="110 40 390 390" role="img" aria-label="Saved layerwise WSG Darcy prediction">
  <image :href="publicAssetUrl('/figures/ch04/darcy_wsg_layerwise.png')" width="630" height="540" />
 </svg>
 <canvas v-else-if="kind==='energy'||kind==='control'" ref="canvas" :aria-label="caption" />
 <svg v-else class="wake-mini" viewBox="1318 330 490 240" role="img" aria-label="Looping saved RFormer reconstructed v-velocity test fields">
  <image :href="urls[index]||publicAssetUrl('/fallback_figures/ch06/vortex.png')" width="1920" height="928" />
 </svg>
 <figcaption>{{caption}}</figcaption>
 <span v-if="failed" class="figure-error">Figure unavailable</span>
</figure>
</template>
<style scoped>
.contribution-figure{width:190px;height:144px;margin:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px}
.contribution-figure svg{display:block;flex-shrink:0}
.encoding-mini{width:190px;height:110px}
.square-mini{width:112px;height:112px}
.wake-mini{width:190px;height:94px}
.energy canvas{width:190px;height:95px;image-rendering:auto}
.control canvas{width:130px;height:130px}
.contribution-figure figcaption{font-size:12px;line-height:16px;text-align:center;width:190px;color:var(--muted)}
.figure-error{font-size:12px}
</style>
