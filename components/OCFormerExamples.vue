<script setup lang="ts">
import {computed,nextTick,onMounted,onBeforeUnmount,ref,watch} from 'vue'
import {useNav} from '@slidev/client'
import * as THREE from 'three'
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls.js'
import {usePlayback} from '../composables/usePlayback'
import {publicAssetUrl} from '../composables/publicAssetUrl.mjs'
const props=defineProps<{mode:'perturbation'|'three-d'}>()
const keys=computed(()=>props.mode==='perturbation'?['perturbation-8','perturbation-16']:['wall','ball'])
const nav=useNav(),staticMode=computed(()=>nav.isPrintMode.value||new URLSearchParams(location.search).has('static'))
const count=ref(200),ready=ref(false),error=ref('')
const {index,playing,active,toggle,pause,seek,reset}=usePlayback(count,0,50)
const {index:rightIndex,playing:rightPlaying,toggle:rightToggle,pause:rightPause,seek:rightSeek,reset:rightReset}=usePlayback(count,0,50)
const panelIndex=(panel:number)=>panel===1?rightIndex.value:index.value
const panelPlaying=(panel:number)=>panel===1?rightPlaying.value:playing.value
const togglePanel=(panel:number)=>panel===1?rightToggle():toggle()
const resetPanel=(panel:number)=>{
 if(panel===1)rightReset();else reset()
 views[panel]?.controls.reset()
}
const seekPanel=(panel:number,value:number)=>panel===1?rightSeek(value):seek(value)
const hosts:HTMLElement[]=[],labels=ref<any[][]>([[],[]]),axisTicks=ref<any[][]>([[],[]])
let meta:any,values:Float32Array,disposed=false,observer:ResizeObserver|undefined
const views:any[]=[]
const point=(c:any,t:number,a:number)=>Array.from({length:c.dimension},(_,j)=>values[c.float_offset+(t*c.agents+a)*c.dimension+j])
function create3D(host:HTMLElement,c:any,panel:number){
 const scene=new THREE.Scene();scene.background=new THREE.Color('white')
 const camera=new THREE.PerspectiveCamera(c.sphere?42:38,1,.01,20);camera.up.set(0,0,1)
 const center=c.extent.map((r:number[])=>(r[0]+r[1])/2)
 camera.position.set(1.6,-2.2,center[2]+1)
 const renderer=new THREE.WebGLRenderer({antialias:true,preserveDrawingBuffer:true});renderer.setPixelRatio(Math.min(devicePixelRatio,2));host.prepend(renderer.domElement)
 const controls=new OrbitControls(camera,renderer.domElement);controls.target.set(...center as [number,number,number]);controls.enablePan=false;controls.minDistance=1.1;controls.maxDistance=5;controls.update();controls.saveState()
 scene.add(new THREE.AmbientLight(0xffffff,2));const light=new THREE.DirectionalLight(0xffffff,2);light.position.set(2,-2,3);scene.add(light)
 const room=new THREE.BoxGeometry(...c.extent.map((r:number[])=>r[1]-r[0]) as [number,number,number]);const edges=new THREE.LineSegments(new THREE.EdgesGeometry(room),new THREE.LineBasicMaterial({color:0xbbc0bd,transparent:true,opacity:.6}));edges.position.set(...center as [number,number,number]);scene.add(edges);room.dispose()
 for(const b of c.barriers){
  const geometry=new THREE.BoxGeometry(...b.map((r:number[])=>r[1]-r[0]) as [number,number,number])
  const box=new THREE.Mesh(geometry,new THREE.MeshLambertMaterial({color:0xbfc6c2,transparent:true,opacity:.3,depthWrite:false}));box.position.set(...b.map((r:number[])=>(r[0]+r[1])/2) as [number,number,number]);scene.add(box)
  const edge=new THREE.LineSegments(new THREE.EdgesGeometry(geometry),new THREE.LineBasicMaterial({color:0x68766f}));edge.position.copy(box.position);scene.add(edge)
 }
 if(c.sphere){
  const sphere=new THREE.Mesh(new THREE.SphereGeometry(c.sphere.radius,32,20),new THREE.MeshLambertMaterial({color:0xbfc6c2,transparent:true,opacity:.4,depthWrite:false}));sphere.position.fromArray(c.sphere.center);scene.add(sphere)
 }
 const drones=new THREE.InstancedMesh(new THREE.SphereGeometry(c.radius,10,8),new THREE.MeshLambertMaterial(),c.agents)
 c.colors.forEach((color:string,a:number)=>drones.setColorAt(a,new THREE.Color(color)));drones.instanceMatrix.setUsage(THREE.DynamicDrawUsage);scene.add(drones)
 const trails:THREE.Line[]=[]
 for(let a=0;a<c.agents;a++){
  const coordinates=new Float32Array(600);for(let t=0;t<200;t++)coordinates.set(point(c,t,a),t*3)
  const g=new THREE.BufferGeometry();g.setAttribute('position',new THREE.BufferAttribute(coordinates,3));g.setDrawRange(0,1)
  const line=new THREE.Line(g,new THREE.LineBasicMaterial({color:0x89958d,transparent:true,opacity:.2}));scene.add(line);trails.push(line)
 }
 const v={scene,camera,renderer,controls,drones,trails,host,c,panel};views.push(v);controls.addEventListener('change',()=>render3D(v));return v
}
function render3D(v:any){
 const {host,camera,renderer}=v,w=host.clientWidth,h=host.clientHeight
 if(!w||!h)return
 camera.aspect=w/h;camera.updateProjectionMatrix();renderer.setSize(w,h,false);renderer.render(v.scene,camera)
 const extent=v.c.extent,center=extent.map((r:number[])=>(r[0]+r[1])/2)
 const project=(p:number[])=>{
  const q=new THREE.Vector3(...p as [number,number,number]).project(camera)
  const halfWidth=w/2,halfHeight=h/2
  return{x:halfWidth+q.x*halfWidth,y:halfHeight-q.y*halfHeight}
 }
 const origin=project(center),nearX=camera.position.x>=center[0]?extent[0][1]:extent[0][0],nearY=camera.position.y>=center[1]?extent[1][1]:extent[1][0]
 const farX=nearX===extent[0][0]?extent[0][1]:extent[0][0],floor=extent[2][0]
 const axes=[{name:'x',axis:0,base:[center[0],nearY,floor]},{name:'y',axis:1,base:[nearX,center[1],floor]},{name:'z',axis:2,base:[farX,nearY,center[2]]}]
 const entries:any[]=[],ticks:any[]=[]
 for(const axis of axes){
  const at=(value:number)=>{const p=[...axis.base];p[axis.axis]=value;return project(p)}
  const [lo,hi]=extent[axis.axis],a=at(lo),b=at(hi),length=Math.hypot(b.x-a.x,b.y-a.y)
  if(length<50)continue
  const tx=(b.x-a.x)/length,ty=(b.y-a.y)/length,mid=at((lo+hi)/2)
  let nx=-ty,ny=tx;if(nx*(mid.x-origin.x)+ny*(mid.y-origin.y)<0){nx=-nx;ny=-ny}
  entries.push({id:axis.name,text:axis.name,left:mid.x+nx*34,top:mid.y+ny*34})
  const values=axis.axis===2?(v.c.sphere?[-.5,0,.5]:[0,.5,1]):[-.5,0,.5]
  values.forEach((value,i)=>{
   const p=at(value),along=i===0?12:i===values.length-1?-12:0
   ticks.push({id:axis.name+i,x1:p.x,y1:p.y,x2:p.x+nx*5,y2:p.y+ny*5})
   entries.push({id:axis.name+i,text:String(value).replace('-', '−'),left:p.x+nx*15+tx*along,top:p.y+ny*15+ty*along})
  })
 }
 labels.value[v.panel]=entries;axisTicks.value[v.panel]=ticks

}
function draw(){
 if(!ready.value)return
 keys.value.forEach((key,panel)=>{
  const t=staticMode.value?99:props.mode==='three-d'?panelIndex(panel):index.value
  const c=meta.cases[key],host=hosts[panel];if(!host)return
  if(c.dimension===3){
   const v=views[panel],m=new THREE.Matrix4();for(let a=0;a<c.agents;a++){m.makeTranslation(...point(c,t,a) as [number,number,number]);v.drones.setMatrixAt(a,m);v.trails[a].geometry.setDrawRange(0,t+1)}
   v.drones.instanceMatrix.needsUpdate=true;v.drones.computeBoundingSphere();render3D(v)
  }else{
   const canvas=host.querySelector('canvas')!,size=host.clientWidth,ratio=devicePixelRatio||1;canvas.width=size*ratio;canvas.height=size*ratio
   const ctx=canvas.getContext('2d')!;ctx.scale(ratio,ratio);ctx.clearRect(0,0,size,size)
   const pad=16,span=size-2*pad,x=(n:number)=>pad+(n+.6)/1.2*span,y=(n:number)=>pad+(.6-n)/1.2*span
   ctx.lineWidth=.7;ctx.strokeStyle='#aab1ae';ctx.strokeRect(pad,pad,span,span)
   ctx.fillStyle='#59635f';ctx.font='12px "Noto Serif"';ctx.textAlign='center';for(const n of [-.5,0,.5]){ctx.fillText(String(n),x(n),size-3);}
   labels.value[panel]=[-.5,0,.5].map(n=>({text:String(n),left:2,top:y(n)}))
   for(let a=0;a<c.agents;a++){
    ctx.beginPath();ctx.strokeStyle='rgba(105,115,110,.2)';for(let k=0;k<=t;k++){const p=point(c,k,a);if(!k)ctx.moveTo(x(p[0]),y(p[1]));else ctx.lineTo(x(p[0]),y(p[1]))}ctx.stroke()
    const ref=c.reference[0][a],start=c.boundary[0][a],end=c.boundary[1][a]
    ctx.strokeStyle='#abb2af';ctx.beginPath();ctx.arc(x(ref[0]),y(ref[1]),2.4,0,Math.PI*2);ctx.stroke()
    ctx.beginPath();ctx.moveTo(x(ref[0]),y(ref[1]));ctx.lineTo(x(start[0]),y(start[1]));ctx.stroke()
    ctx.strokeStyle=c.colors[a];ctx.beginPath();ctx.moveTo(x(end[0])-2,y(end[1])-2);ctx.lineTo(x(end[0])+2,y(end[1])+2);ctx.moveTo(x(end[0])+2,y(end[1])-2);ctx.lineTo(x(end[0])-2,y(end[1])+2);ctx.stroke()
    const p=point(c,t,a);ctx.lineWidth=1.2;ctx.beginPath();ctx.arc(x(p[0]),y(p[1]),c.radius/1.2*span,0,2*Math.PI);ctx.stroke();ctx.lineWidth=.7
   }
  }
 })
}
watch([index,rightIndex,staticMode],draw);watch(staticMode,v=>{if(v){pause();rightPause()}});watch(active,v=>{if(v)draw()})
onMounted(async()=>{
 try{
  const r=await fetch(publicAssetUrl('/data/ch07/ocformer-examples/index.json'));if(!r.ok)throw Error('Index unavailable');meta=await r.json()
  const b=await fetch(publicAssetUrl(meta.binary.path));if(!b.ok)throw Error('Trajectories unavailable');const bytes=await b.arrayBuffer()
  const hash=Array.from(new Uint8Array(await crypto.subtle.digest('SHA-256',bytes))).map(v=>v.toString(16).padStart(2,'0')).join('')
  if(hash!==meta.binary.sha256||bytes.byteLength!==meta.binary.byte_length||meta.frame_count!==200||meta.dtype!=='float32'||meta.byte_order!=='little')throw Error('Invalid trajectory data')
  values=new Float32Array(bytes);if(!values.every(Number.isFinite))throw Error('Invalid coordinates')
  for(const key of keys.value){const c=meta.cases[key];if(c.shape.join(',')!==`200,${c.agents},${c.dimension}`||c.float_offset<0||c.float_offset+200*c.agents*c.dimension>values.length)throw Error('Invalid case shape')}
  if(disposed)return
  await nextTick();keys.value.forEach((key,panel)=>{const c=meta.cases[key];if(c.dimension===3)create3D(hosts[panel],c,panel)})
  ready.value=true;observer=new ResizeObserver(draw);hosts.forEach(h=>observer!.observe(h));draw()
 }catch(e){if(!disposed)error.value=String(e)}
})
onBeforeUnmount(()=>{disposed=true;observer?.disconnect();for(const v of views){v.controls.dispose();v.scene.traverse((o:any)=>{o.geometry?.dispose();if(o.material){for(const m of Array.isArray(o.material)?o.material:[o.material])m.dispose()}});v.renderer.dispose()}})
</script>
<template>
 <section class="oc-examples" :class="mode" @click.stop @pointerdown.stop @keydown.stop>
  <div class="oc-panels">
   <figure v-for="(key,panel) in keys" :key="key">
    <figcaption>{{key==='ball'?'Drones in a 3D room':key==='wall'?'Drones go over a wall':`${key==='perturbation'?32:key.split('-')[1]} drones`}}</figcaption>
    <div class="oc-viewport" :ref="el=>{if(el)hosts[panel]=el as HTMLElement}">
     <canvas v-if="mode==='perturbation'" :aria-label="`${key==='perturbation'?32:key.split('-')[1]}-drone transferred trajectory`" />
     <svg v-if="mode==='three-d'" class="oc-axis-ticks" aria-hidden="true"><line v-for="tick in axisTicks[panel]" :key="tick.id" :x1="tick.x1" :y1="tick.y1" :x2="tick.x2" :y2="tick.y2" /></svg>
     <span v-for="label in labels[panel]" :key="label.id||label.text" class="oc-axis" :class="{'math-axis':['x','y','z'].includes(label.text)}" :style="{left:label.left+'px',top:label.top+'px'}">{{label.text}}</span>
    </div>
    <p v-if="mode==='three-d'" class="oc-key">{{key==='ball'?'16 agents exchange antipodal positions around a central sphere.':'100 agents navigate the two wall-like barriers.'}}</p>
    <div v-if="mode==='three-d'&&ready&&!staticMode" class="plot-controls"><button @click="togglePanel(panel)">{{panelPlaying(panel)?'Pause':'Play'}}</button><button @click="resetPanel(panel)">Reset</button><input class="playback-slider" :style="{'--progress':`${100*panelIndex(panel)/199}%`}" :aria-label="`${key} physical time`" type="range" min="0" max="199" :value="panelIndex(panel)" @input="seekPanel(panel,Number(($event.target as HTMLInputElement).value))"><output>{{meta.times[panelIndex(panel)].toFixed(2)}} s</output></div>
   </figure>
  </div>
  <p v-if="mode==='perturbation'" class="oc-legend">Colored circles: agents · gray circles: original starts · ×: targets</p>
  <div v-if="mode==='perturbation'&&ready&&!staticMode" class="plot-controls"><button @click="toggle">{{playing?'Pause':'Play'}}</button><button @click="reset">Reset</button><input class="playback-slider" :style="{'--progress':`${100*index/199}%`}" aria-label="Trajectory physical time" type="range" min="0" max="199" :value="index" @input="seek(Number(($event.target as HTMLInputElement).value))"><output>{{meta.times[index].toFixed(2)}} s</output></div>
  <p v-if="error" role="status">{{error}}</p><p v-else-if="!ready" role="status">Loading saved trajectories…</p>
 </section>
</template>
<style scoped>
.oc-panels{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px}
.perturbation .oc-panels{grid-template-columns:repeat(2,260px);gap:10px 16px;justify-content:center}
figure{margin:0;min-width:0}figcaption{font-size:16px;font-weight:600;text-align:center;margin-bottom:6px;line-height:22px}
.oc-viewport{height:340px;position:relative;width:100%}
.perturbation figcaption{margin-bottom:2px}
.perturbation .plot-controls{margin-top:8px}
.perturbation .oc-viewport{width:210px;height:210px;margin:0 auto}
.oc-examples.perturbation .oc-legend{font-size:12px;line-height:17px;text-align:center;margin:6px 0 0}
.oc-viewport :deep(canvas){display:block;width:100%;height:100%}
.oc-axis-ticks{position:absolute;inset:0;width:100%;height:100%;overflow:visible;pointer-events:none}
.oc-axis-ticks line{stroke:#8b9590;stroke-width:1}
.oc-axis{position:absolute;font-size:12px;line-height:16px;transform:translate(-50%,-50%);pointer-events:none}
.math-axis{font-family:KaTeX_Math;font-style:italic}
.oc-key{font-size:14px;line-height:1.4;text-align:center;margin:8px 0 0}
.plot-controls{margin:10px 0 0;font-size:12px;gap:8px}
</style>
