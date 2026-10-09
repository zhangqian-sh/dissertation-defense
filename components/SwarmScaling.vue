<script setup lang="ts">
import {computed,onMounted,onBeforeUnmount,ref,watch} from 'vue'
import {useNav} from '@slidev/client'
import {usePlayback} from '../composables/usePlayback'
import {publicAssetUrl} from '../composables/publicAssetUrl.mjs'
const nav=useNav(),staticMode=computed(()=>nav.isPrintMode.value||['static','print'].some(k=>new URLSearchParams(location.search).has(k)))
const ready=ref(false),error=ref(''),count=ref(200)
const {index,playing,toggle,pause,seek,reset}=usePlayback(count,0,50)
const cases=[8,16,32,128],canvases:HTMLCanvasElement[]=[]
let meta:any,values:Float32Array,disposed=false,observer:ResizeObserver|undefined
const point=(c:any,t:number,a:number,axis:number)=>values[c.float_offset+(t*c.agents+a)*2+axis]
function draw(){
 if(!ready.value)return
 const t=staticMode.value?99:index.value
 meta.cases.forEach((c:any,panel:number)=>{
  const canvas=canvases[panel];if(!canvas)return
  const size=canvas.clientWidth,ratio=window.devicePixelRatio||1
  canvas.width=Math.round(size*ratio);canvas.height=Math.round(size*ratio)
  const ctx=canvas.getContext('2d')!;ctx.scale(ratio,ratio);ctx.fillStyle='white';ctx.fillRect(0,0,size,size)
  const x=(v:number)=>(v+.52)/1.04*size,y=(v:number)=>(.52-v)/1.04*size
  ctx.lineWidth=.8;ctx.strokeStyle='rgba(110,110,110,.14)'
  for(let agent=0;agent<c.agents;agent++){
   ctx.beginPath();for(let k=0;k<=t;k++){const px=x(point(c,k,agent,0)),py=y(point(c,k,agent,1));if(!k)ctx.moveTo(px,py);else ctx.lineTo(px,py)}ctx.stroke()
  }
  ctx.lineWidth=1.1
  for(let agent=0;agent<c.agents;agent++){
   ctx.strokeStyle=c.colors[agent];ctx.beginPath();ctx.arc(x(point(c,t,agent,0)),y(point(c,t,agent,1)),c.radius/1.04*size,0,2*Math.PI);ctx.stroke()
  }
 })
}
watch([index,staticMode],draw)
watch(staticMode,v=>{if(v)pause()})
onMounted(async()=>{
 observer=new ResizeObserver(draw);canvases.forEach(canvas=>observer!.observe(canvas))
 try{
  const r=await fetch(publicAssetUrl('/data/ch07/swarm-scaling/index.json'));if(!r.ok)throw Error('Missing trajectory index');const d=await r.json()
  if(d.dtype!=='float32'||d.byte_order!=='little'||d.times.length!==200||!d.times.every((t:number,i:number)=>Number.isFinite(t)&&(!i||t>d.times[i-1]))||d.frame_count!==200||d.cases.length!==4||!d.cases.every((c:any,i:number)=>c.agents===cases[i]&&c.shape.join(',')===`200,${cases[i]},2`))throw Error('Invalid trajectory shapes')
  const b=await fetch(publicAssetUrl(d.binary.path));if(!b.ok)throw Error('Missing trajectories');const bytes=await b.arrayBuffer()
  const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))).map(v=>v.toString(16).padStart(2,'0')).join('')
  if(hash!==d.binary.sha256||bytes.byteLength!==d.binary.byte_length)throw Error('Trajectory checksum mismatch')
  values=new Float32Array(bytes);let offset=0
  for(const c of d.cases){if(c.float_offset!==offset||c.colors.length!==c.agents)throw Error('Invalid trajectory offset');offset+=200*c.agents*2}
  if(offset!==values.length||!values.every(Number.isFinite))throw Error('Invalid trajectory values')
  if(disposed)return;meta=d;ready.value=true;draw()
 }catch(e){if(!disposed)error.value='Trajectory data unavailable'}
})
onBeforeUnmount(()=>{disposed=true;observer?.disconnect()})
const ticks=[{value:'−0.5',percent:100*.02/1.04},{value:'0',percent:50},{value:'0.5',percent:100*1.02/1.04}]
</script>
<template>
 <section class="swarm-scaling" @click.stop @pointerdown.stop @keydown.stop>
  <div class="swarm-scaling-grid">
   <figure v-for="(agents,i) in cases" :key="agents" class="swarm-scaling-panel">
    <figcaption>{{agents}} drones</figcaption>
    <div class="swarm-scaling-axes">
     <canvas :ref="element=>{if(element)canvases[i]=element as HTMLCanvasElement}" :aria-label="`${agents} drones at frame ${staticMode?100:index+1} of 200`" />
     <span v-for="tick in ticks" :key="'x'+tick.value" class="swarm-x-tick" :style="{left:tick.percent+'%'}">{{tick.value}}</span>
     <span v-for="tick in ticks" :key="'y'+tick.value" class="swarm-y-tick" :style="{bottom:tick.percent+'%'}">{{tick.value}}</span>
     <span class="swarm-x-label"><InlineMath tex="x" /></span><span class="swarm-y-label"><InlineMath tex="y" /></span>
    </div>
   </figure>
  </div>
  <div v-if="ready&&!staticMode" class="plot-controls"><button @click="toggle">{{playing?'Pause':'Play'}}</button><button @click="reset">Reset</button><input class="playback-slider" :style="{'--progress':`${100*index/199}%`}" aria-label="Swarm physical time" type="range" min="0" max="199" :value="index" @input="seek(Number(($event.target as HTMLInputElement).value))"><output>{{meta.times[index].toFixed(2)}} s</output></div>
  <p v-if="error" role="status">{{error}}</p><p v-else-if="!ready" role="status">Loading saved trajectories…</p>
 </section>
</template>
<style scoped>
.swarm-scaling-grid{display:grid;grid-template-columns:repeat(2,210px);gap:12px;justify-content:center}
.swarm-scaling-panel{margin:0;min-width:0;display:flex;flex-direction:column;align-items:center;padding-bottom:26px}
.swarm-scaling-panel figcaption{font-size:16px;font-weight:600;line-height:22px;margin-bottom:4px}
.swarm-scaling-axes{position:relative;width:170px;height:170px;border-left:1px solid #596361;border-bottom:1px solid #596361}
canvas{display:block;width:100%;height:100%}
.swarm-x-tick,.swarm-y-tick{position:absolute;font-size:12px;line-height:16px;white-space:nowrap}
.swarm-x-tick{top:calc(100% + 2px);transform:translateX(-50%)}
.swarm-y-tick{right:calc(100% + 5px);transform:translateY(50%)}
.swarm-x-label{position:absolute;top:calc(100% + 18px);left:50%;transform:translateX(-50%);font-size:12px}
.swarm-y-label{position:absolute;right:calc(100% + 34px);top:50%;transform:translateY(-50%) rotate(-90deg);font-size:12px}
.plot-controls{font-size:12px;margin-top:8px;gap:8px}
</style>
