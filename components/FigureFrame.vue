<script setup lang="ts">
import { publicAssetUrl } from '../composables/publicAssetUrl.mjs'
defineProps<{fallback:string;ready:boolean;error?:string;staticMode?:boolean;caption:string}>()
</script>
<template>
  <section class="interactive-figure" @keydown.stop @pointerdown.stop @click.stop @wheel.stop>
    <template v-if="ready && !staticMode && !error"><slot /></template>
    <template v-else><img class="figure-fallback" :src="publicAssetUrl(fallback)" :alt="caption"><div v-if="error" role="status" class="status-note">Static view · interactive data unavailable</div><div v-else-if="!staticMode" class="status-note">Loading recorded data…</div></template>
    <div class="interaction-note">{{ caption }}</div>
  </section>
</template>
