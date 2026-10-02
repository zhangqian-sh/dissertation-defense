<script setup lang="ts">
import {ref} from 'vue'
const mode=ref('2d')
</script>
<template>
 <div class="swarm-tabs" @click.stop @keydown.stop><button :aria-pressed="mode==='2d'" @click="mode='2d'">2D · 128 drones</button><button :aria-pressed="mode==='3d'" @click="mode='3d'">3D · 16 drones</button></div>
 <DroneSwarm3D v-if="mode==='3d'" />
 <RecordedSequence v-else name="swarm128" label="128-drone physical time" caption="2D per-instance · M=128, radius 0.01 · 200 saved frames · clearance = min pair distance − 0.02; sampled, not continuous-time safety." />
</template>
<style scoped>
.swarm-tabs{display:flex;gap:10px;margin-bottom:6px}
button{font-size:12px;padding:4px 12px;background:white;border:1px solid #c9cfcd;border-radius:3px}
button[aria-pressed=true]{color:var(--brown);border-color:var(--brown)}
</style>
