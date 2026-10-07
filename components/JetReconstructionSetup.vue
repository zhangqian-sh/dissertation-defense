<script setup lang="ts">
// Derive both camera rotation and sightline start from the same lens axis.
const cameras=[{x:37,y:48,tx:149,ty:88},{x:32,y:171,tx:145,ty:177},{x:351,y:47,tx:240,ty:89},{x:354,y:183,tx:237,ty:182}].map(c=>{
 const y=20+1.7*c.y,ty=20+1.7*c.ty
 const angle=Math.atan2(ty-y,c.tx-c.x),dx=Math.cos(angle),dy=Math.sin(angle)
 return {...c,y,ty,angle:angle*180/Math.PI,lensX:c.x+21*dx,lensY:y+21*dy}
})
const particles=Array.from({length:72},(_,i)=>({x:185+Math.sin(i*2.4)*31,duration:4.8,phase:i/72,y:230-170*i/72}))
</script>
<template>
<div class="jet-apparatus" role="img" aria-label="Schematic of a seeded round water jet entering a 3D measurement volume, observed by four high-speed cameras for particle tracking velocimetry">
<div class="jet-apparatus-drawing">
<svg viewBox="0 0 424 505" preserveAspectRatio="xMidYMid meet" aria-hidden="true">
  <!-- Sightlines leave each lens along its optical axis. -->
  <g fill="none" stroke="#98a4ae" stroke-width="1" stroke-dasharray="4 4">
    <path v-for="(c,i) in cameras" :key="i" :d="`M${c.lensX} ${c.lensY} L${c.tx} ${c.ty}`"/>
  </g>
  <g transform="translate(0 20) scale(1 1.7)">
  <!-- Transparent measurement volume. -->
  <path d="M132 62 L181 35 H266 L217 62 Z" fill="#eef3f5" fill-opacity=".65" stroke="#98a4ae"/>
  <path d="M217 62 L266 35 V203 L217 230 Z" fill="#eef3f5" fill-opacity=".35" stroke="#98a4ae"/>
  <path d="M132 62 H217 V230 H132 Z" fill="#eef3f5" fill-opacity=".35" stroke="#98a4ae"/>
  <path d="M181 35 V203 H266 M132 230 L181 203" fill="none" stroke="#98a4ae" stroke-dasharray="4 4"/>
  <!-- Widening jet and schematic seeding particles. -->
  <path d="M178 230 C175 184 163 118 152 60 L218 60 C205 128 197 184 192 230 Z" fill="#7895a6" fill-opacity=".18"/>
  <g fill="#8b242d"><ellipse v-for="(p,i) in particles" :key="i" :cx="p.x" :cy="p.y" rx="1.6" ry="0.94">
    <animate attributeName="cy" from="230" to="60" :dur="`${p.duration}s`" :begin="`${-p.phase*p.duration}s`" repeatCount="indefinite"/>
    <animate attributeName="cx" from="185" :to="p.x" :dur="`${p.duration}s`" :begin="`${-p.phase*p.duration}s`" repeatCount="indefinite"/>
  </ellipse></g>
  <!-- Round nozzle feeds the jet from below. -->
  <path d="M177 238 V268 H193 V238" fill="#dce1df" stroke="#596361" stroke-width="1.2"/>
  <ellipse cx="185" cy="238" rx="8" ry="3" fill="white" stroke="#596361" stroke-width="1.2"/>
  <path d="M177 256 H88 M266 97 H306" fill="none" stroke="#596361" stroke-width="1"/>
  </g>
  <g v-for="(c,i) in cameras" :key="i" :transform="`translate(${c.x} ${c.y}) rotate(${c.angle})`">
    <path d="M-18 -11 L-12 -16 H12 L6 -11 Z" fill="#dce1df" stroke="#596361"/>
    <path d="M6 -11 L12 -16 V6 L6 11 Z" fill="#c4cbce" stroke="#596361"/>
    <rect x="-18" y="-11" width="24" height="22" rx="2" fill="#f6f5f4" stroke="#596361"/>
    <rect x="6" y="-6" width="12" height="12" fill="#98a4ae" stroke="#596361"/>
    <ellipse cx="18" cy="0" rx="3" ry="6" fill="#232727"/>
  </g>
</svg>
<span class="jet-camera-label">Four high-speed cameras</span>
<span class="jet-volume-label">Measurement<br>volume</span>
<span class="jet-nozzle-label">Round nozzle</span>
</div>
</div>
</template>
<style scoped>
.jet-apparatus{display:flex;align-items:center;width:100%;height:450px;font-size:16px;color:#596361}
.jet-apparatus-drawing{position:relative;width:100%;aspect-ratio:424 / 505}
.jet-apparatus svg{display:block;width:100%;height:100%}
.jet-apparatus svg path{vector-effect:non-scaling-stroke}
.jet-apparatus-drawing>span{position:absolute;line-height:1.3;white-space:nowrap}
.jet-camera-label{top:0;left:50%;transform:translateX(-50%)}
.jet-volume-label{top:40%;right:0}
.jet-nozzle-label{top:89%;left:3%;transform:translateY(-100%)}
</style>
