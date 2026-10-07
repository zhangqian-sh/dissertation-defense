<script setup lang="ts">
import { computed } from 'vue'
import katex from 'katex'
const props=defineProps<{tex:string}>()
const rendered=computed(()=>katex.renderToString(props.tex,{throwOnError:true}))
</script>
<template><span class="inline-math" v-html="rendered"/></template>
<style scoped>.inline-math :deep(.katex){font-size:1em}</style>
