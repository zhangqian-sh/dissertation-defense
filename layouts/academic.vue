<script setup lang="ts">
import { computed } from 'vue'
import { useSlideContext } from '@slidev/client'
import { publicAssetUrl } from '../composables/publicAssetUrl.mjs'
const props = defineProps<{ chapter?: string; section?: string; source?: string; cover?: boolean; crunchhead?: boolean; divider?: 'chapter' | 'part' }>()
const { $page } = useSlideContext()
const chapterNames: Record<string, string> = {
  "1": "Introduction",
  "2": "Exploratory Studies on Spiking Representations",
  "3": "Calibrated Conversion and Neuromorphic Deployment",
  "4": "Direct SNN Training with Randomized Forward-Mode Gradients",
  "5": "Reconstruction from Sparse Measurements: An Energy Transformer Approach",
  "6": "Reconstruction from Sparse Measurements: A Mesh-Free Approach with In-Context Learning",
  "7": "OCFormer: Physics-Informed Transformers for High-Dimensional Optimal Control",
  "8": "Summary"
}
const headerTitle = computed(() => (props.divider ? props.section : chapterNames[props.chapter || '']) || props.section || 'Doctoral dissertation defense')
</script>
<template>
  <div class="slidev-layout academic" :class="{cover, 'chapter-divider': !!divider, 'part-divider': divider === 'part'}">
    <header class="topline">
      <span>{{ cover ? '' : headerTitle }}</span>
      <div class="progress" aria-hidden="true"><i v-for="n in 8" :key="n" :class="{done:n<=Number(chapter)}" /></div>
    </header>
    <main class="slide-body"><slot /></main>
    <img v-if="crunchhead" class="cover-crunchhead" :src="publicAssetUrl('/figures/shared/crunchhead.png')" alt="Crunchhead illustration" />
    <footer class="footer"><span class="page">{{ chapter ? `CH ${chapter} · ` : '' }}{{ String($page).padStart(2,'0') }}</span></footer>
  </div>
</template>
