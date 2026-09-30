<script setup lang="ts">
import { computed, ref, watch, nextTick, onBeforeUnmount } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/addons/controls/OrbitControls.js'
import { useDefenseAsset } from '../composables/useDefenseAsset'
import { usePlayback } from '../composables/usePlayback'
const {payload:p,error,staticMode}=useDefenseAsset('ch07/ocformer_swarm_3d')
const count=computed(()=>p.value?.time.shape[0]||200)
const {index,playing,active,toggle,seek,reset}=usePlayback(count,0,65)
const host=ref<HTMLDivElement>();const webglError=ref('')
let renderer:THREE.WebGLRenderer|undefined, scene:THREE.Scene, camera:THREE.PerspectiveCamera, controls:OrbitControls, mesh:THREE.InstancedMesh, observer:ResizeObserver
const event=computed(()=>p.value?.critical_events.find((e:any)=>e.trace_id==='pairwise_margin'))
const atEvent=computed(()=>event.value && index.value===event.value.time_index)
const traces=computed(()=>p.value?['pairwise_margin','sphere_distance_margin'].map((name,i)=>({name:i?'Sphere distance':'Pairwise',color:i?'#b27a29':'#287e83',y:p.value.clearance_traces.find((t:any)=>t.id===name).values.values})):[])
function render(){if(renderer&&active.value)renderer.render(scene,camera)}
function update(){if(!renderer||!p.value)return;const matrix=new THREE.Matrix4();const data=p.value.positions.values;const n=p.value.agent_ids.shape[0];for(let i=0;i<n;i++){const k=(index.value*n+i)*3;matrix.makeTranslation(data[k],data[k+1],data[k+2]);mesh.setMatrixAt(i,matrix);mesh.setColorAt(i,new THREE.Color(atEvent.value&&event.value.agent_ids.includes(i)?'#c22d32':'#287e83'))}mesh.instanceMatrix.needsUpdate=true;if(mesh.instanceColor)mesh.instanceColor.needsUpdate=true;render()}
function resetCamera(){if(!camera)return;camera.position.set(1.0,.8,1.2);controls.target.set(0,0,0);controls.update();render()}
function dispose(){observer?.disconnect();controls?.dispose();if(scene)scene.traverse((o:any)=>{o.geometry?.dispose();if(o.material){const materials=Array.isArray(o.material)?o.material:[o.material];materials.forEach((m:any)=>m.dispose())}});renderer?.dispose();renderer=undefined}
async function init(){await nextTick();if(renderer||!host.value||!p.value||staticMode.value)return;try{
  scene=new THREE.Scene();scene.background=new THREE.Color('#fafbf9');camera=new THREE.PerspectiveCamera(38,1,.01,20)
  renderer=new THREE.WebGLRenderer({antialias:true,alpha:false});renderer.setPixelRatio(Math.min(devicePixelRatio,2));host.value.appendChild(renderer.domElement);renderer.domElement.setAttribute('aria-label','Three-dimensional swarm; drag to orbit, wheel to zoom')
  renderer.domElement.addEventListener('webglcontextlost',(e)=>{e.preventDefault();webglError.value='WebGL context lost'})
  controls=new OrbitControls(camera,renderer.domElement);controls.enableDamping=false;controls.minDistance=.3;controls.maxDistance=4;controls.addEventListener('change',render)
  scene.add(new THREE.AmbientLight(0xffffff,2));const light=new THREE.DirectionalLight(0xffffff,2);light.position.set(2,3,4);scene.add(light)
  const obs=p.value.obstacles[0];const sphere=new THREE.Mesh(new THREE.SphereGeometry(obs.radius,32,20),new THREE.MeshStandardMaterial({color:'#b4a08d',transparent:true,opacity:.32,depthWrite:false}));sphere.position.fromArray(obs.center);scene.add(sphere)
  const n=p.value.agent_ids.shape[0];mesh=new THREE.InstancedMesh(new THREE.SphereGeometry(p.value.agent_radius,16,10),new THREE.MeshStandardMaterial({color:'white'}),n);scene.add(mesh)
  const coords=p.value.positions.values;for(let i=0;i<n;i++){const pts=[];for(let t=0;t<count.value;t++){const k=(t*n+i)*3;pts.push(new THREE.Vector3(coords[k],coords[k+1],coords[k+2]))}scene.add(new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts),new THREE.LineBasicMaterial({color:'#527c81',transparent:true,opacity:.4})))}
  const grid=new THREE.GridHelper(1.2,6,'#c3ceca','#e0e6e2');grid.position.y=-.52;scene.add(grid)
  const resize=()=>{if(!host.value||!renderer)return;const w=host.value.clientWidth,h=host.value.clientHeight;if(!w||!h)return;renderer.setSize(w,h);camera.aspect=w/h;camera.updateProjectionMatrix();render()}
  observer=new ResizeObserver(resize);observer.observe(host.value);resize();resetCamera();update()
}catch(e){dispose();webglError.value=String(e)}}
watch([p,host],init,{flush:'post'});watch(index,update);watch(active,(v)=>{if(v){init();render()}});onBeforeUnmount(dispose)
</script>
<template>
<FigureFrame fallback="/fallback_figures/ch07/ocformer_swarm_3d.png" :ready="!!p" :error="error||webglError" :static-mode="staticMode" caption="Per-instance 3D sphere case · agent radius 0.02; center-exclusion sphere radius 0.1 · sampled position constraints, not continuous-time safety.">
  <div class="swarm-layout"><div><div ref="host" class="swarm-canvas"/><div class="micro">Drag to orbit · scroll to zoom · benchmark coordinates</div></div><div><div class="legend"><span v-for="s in traces" :key="s.name" :style="{'--series':s.color}">{{s.name}}</span></div><TracePlot :x="p.time.values" :series="traces" :cursor="index" :height="220" :width="470" x-label="physical time · s" y-label="margin · benchmark length" @seek="seek"/><div class="event-readout">Closest pair: agents {{event.agent_ids.join(' & ')}} · t={{event.time.toFixed(4)}} s<br>Margin {{event.clearance.toExponential(3)}} · {{atEvent?'highlighted in red':'jump to inspect'}}</div></div></div>
  <div class="plot-controls"><button @click="toggle">{{playing?'Pause':'Play'}}</button><button @click="reset">Reset</button><input aria-label="Swarm physical time" type="range" min="0" :max="count-1" :value="index" @input="seek(Number(($event.target as HTMLInputElement).value))"><output>{{p.time.values[index].toFixed(3)}} s</output><button @click="seek(event.time_index)">Closest pair</button><button @click="resetCamera">Reset camera</button></div>
</FigureFrame>
</template>
