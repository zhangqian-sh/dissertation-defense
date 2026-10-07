<script setup lang="ts">
import katex from 'katex'
const math = (tex: string) => katex.renderToString(tex,{throwOnError:true})
</script>
<template>
<div class="et-horizontal-flow" role="img" aria-label="Tokens flow left to right through layer normalization, parallel MHA and Hopfield energies, energy summation, a gradient step, and addition of the original token state.">
<svg viewBox="0 0 530 190" preserveAspectRatio="none" aria-hidden="true">
  <g class="et-shafts">
    <path d="M32 92 H51 M110 92 H134 V48 H154 M134 92 V136 H154"/>
    <path d="M292 48 H320 V78 M292 136 H320 V106"/>
    <path d="M330 92 H346 M429 92 H436 M460 92 H474"/>
    <path d="M38 92 V176 H450 V106"/>
  </g>
  <g class="et-heads">
    <polygon points="55,92 47,88 47,96"/>
    <polygon points="158,48 150,44 150,52"/>
    <polygon points="158,136 150,132 150,140"/>
    <polygon points="320,82 316,74 324,74"/>
    <polygon points="320,102 316,110 324,110"/>
    <polygon points="350,92 342,88 342,96"/>
    <polygon points="440,92 432,88 432,96"/>
    <polygon points="478,92 470,88 470,96"/>
    <polygon points="450,102 446,110 454,110"/>
  </g>
  <circle cx="320" cy="92" r="10" class="et-junction"/>
  <circle cx="450" cy="92" r="10" class="et-junction"/>
</svg>
<span class="et-state et-input" v-html="math(String.raw`x^{(t)}`)"/>
<div class="et-flow-node et-ln">LN</div>
<div class="et-flow-node et-mha"><span>MHA energy</span><span v-html="math(String.raw`E_\theta^{\mathrm{MHA}}`)"/></div>
<div class="et-flow-node et-hn"><span>HN energy</span><span v-html="math(String.raw`E_\theta^{\mathrm{HN}}`)"/></div>
<span class="et-sum">+</span>
<div class="et-flow-node et-gradient" v-html="math(String.raw`-\alpha\nabla_g E`)"/>
<span class="et-add">+</span>
<span class="et-state et-output" v-html="math(String.raw`x^{(t+1)}`)"/>
</div>
</template>
<style scoped>
.et-horizontal-flow{position:relative;width:100%;height:190px;font-size:16px}
.et-horizontal-flow>svg{position:absolute;inset:0;width:100%;height:190px}
.et-shafts{fill:none;stroke:#596361;stroke-width:1.6;stroke-linejoin:round}
.et-heads{fill:#596361}.et-junction{fill:white;stroke:#98a4ae;stroke-width:1.2}
.et-flow-node{position:absolute;display:flex;align-items:center;justify-content:center;flex-direction:column;gap:3px;border:1px solid #98a4ae;background:white;height:44px;box-sizing:border-box;line-height:1.15}
.et-ln{left:10.377%;width:10.377%;top:70px}
.et-mha,.et-hn{left:29.811%;width:25.283%;height:56px}
.et-mha{top:20px}.et-hn{top:108px}
.et-gradient{left:66.038%;width:14.906%;top:70px}
.et-state{position:absolute;top:92px;transform:translateY(-50%);text-align:center}
.et-input{left:0;width:6.038%}.et-output{left:90.943%;width:9.057%}
.et-sum,.et-add{position:absolute;top:92px;transform:translate(-50%,-50%);line-height:1;font-size:20px}
.et-sum{left:60.377%}.et-add{left:84.906%}
.et-horizontal-flow :deep(.katex){font-size:1em}
</style>
