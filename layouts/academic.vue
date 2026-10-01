<script setup lang="ts">
import { useSlideContext } from '@slidev/client'
const props = defineProps<{ chapter?: string; section?: string; source?: string; cover?: boolean; divider?: 'chapter' | 'part' }>()
const { $page } = useSlideContext()
</script>
<template>
  <div class="slidev-layout academic" :class="{cover, 'chapter-divider': !!divider, 'part-divider': divider === 'part'}">
    <div class="progress" aria-hidden="true"><i v-for="n in 8" :key="n" :class="{done:n<=Number(chapter)}" /></div>
    <header class="topline"><span>{{ section || 'Doctoral dissertation defense' }}</span><span class="institution">Brown University · Applied Mathematics</span></header>
    <main class="slide-body"><slot /></main>
    <footer class="footer"><span class="source">{{ source || 'Qian Zhang · Doctoral dissertation · Brown University' }}</span><span class="page">{{ chapter ? `CH ${chapter} · ` : '' }}{{ String($page).padStart(2,'0') }}</span></footer>
  </div>
</template>
