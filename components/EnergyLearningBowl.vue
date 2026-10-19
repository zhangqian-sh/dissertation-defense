<script setup lang="ts">
import InlineMath from './InlineMath.vue'
// A schematic energy cross-section in perspective, not a fitted ET landscape.
// Translate the basin to illustrate how supervising its decoded minimizer
// changes the energy parameters; this is not a guarantee of convex ET energy.
const project = (u:number,v:number,center:number) => [center+83*u+25*v,111+19*v-61*(u*u+v*v)]
const curve = (points:number[][]) => points.map((p,i)=>`${i?'L':'M'}${p[0].toFixed(2)},${p[1].toFixed(2)}`).join(' ')
const rim = (center:number) => curve(Array.from({length:97},(_,i)=>{const a=2*Math.PI*i/96;return project(Math.cos(a),Math.sin(a),center)}))+' Z'
const meridians = (center:number) => {
 const paths:string[]=[]
 for(const fixed of [-.75,-.5,-.25,0,.25,.5,.75]){
  const extent=Math.sqrt(1-fixed*fixed)
  for(const transpose of [false,true])paths.push(curve(Array.from({length:49},(_,i)=>{
   const s=-extent+2*extent*i/48
   return transpose?project(fixed,s,center):project(s,fixed,center)
  })))
 }
 return paths
}
const initialCenter=95,learnedCenter=161
const mesh=meridians(learnedCenter)
</script>

<template>
  <figure class="energy-learning-bowl" role="img" aria-label="Schematic initial energy basin in dashed gray and learned energy basin in brown. Training moves the basin's minimum so its decoded state matches the target field. The bowl is illustrative, not an assertion that Energy Transformer energy is globally convex.">
    <svg viewBox="0 0 270 153" aria-hidden="true">
      <path :d="rim(initialCenter)" class="initial" />
      <path v-for="i in [0,1]" :key="i" :d="curve(Array.from({length:49},(_,j)=>{const t=-1+2*j/48;return i?project(0,t,initialCenter):project(t,0,initialCenter)}))" class="initial" />
      <path :d="rim(learnedCenter)" class="surface" />
      <path v-for="(d,i) in mesh" :key="i" :d="d" class="mesh" />
      <path :d="rim(learnedCenter)" class="rim" />
      <circle :cx="initialCenter" cy="111" r="3.2" class="initial-minimum" />
      <path d="M102 122 C118 133 137 133 153 122" class="training-shaft" />
      <polygon points="158,118 151.5,126.8 147.8,121.6" class="training-head" />
      <circle :cx="learnedCenter" cy="111" r="4" class="learned-minimum" />
      <path d="M161 116 V140" class="leader" />
    </svg>
    <span class="initial-label">Initial</span>
    <span class="energy-label"><InlineMath tex="E_\theta" /></span>
    <figcaption><InlineMath tex="D_\theta(x^{(T)})\approx w" /></figcaption>
  </figure>
</template>

<style scoped>
.energy-learning-bowl{position:relative;margin:0;width:100%;height:160px}
svg{display:block;width:100%;height:145px}
.initial{fill:none;stroke:#98a4ae;stroke-width:1;stroke-dasharray:3 3}
.surface{fill:#f4ede4;fill-opacity:.55;stroke:none}
.mesh{fill:none;stroke:#4e3629;stroke-opacity:.42;stroke-width:.7}
.rim{fill:none;stroke:#4e3629;stroke-width:1.1}
.initial-minimum{fill:white;stroke:#98a4ae;stroke-width:1.2}
.training-shaft{fill:none;stroke:#ed1c24;stroke-width:1.5}
.training-head,.learned-minimum{fill:#ed1c24}
.leader{fill:none;stroke:#98a4ae;stroke-width:.8}
.initial-label{position:absolute;top:1px;left:5px;font-size:12px;color:#596361}
.energy-label{position:absolute;top:1px;right:5px;font-size:16px}
.energy-learning-bowl figcaption{position:absolute;bottom:0;left:26%;right:0;text-align:center;font-size:14px;line-height:1.4}
</style>
