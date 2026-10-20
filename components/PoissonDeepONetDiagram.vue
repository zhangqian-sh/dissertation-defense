<script setup lang="ts">
import InlineMath from './InlineMath.vue'
</script>

<template>
  <figure class="deeponet-network" aria-label="DeepONet: sampled forcing enters a real-valued branch; the coordinate enters spike encoding and a hybrid spiking trunk; their features combine by inner product">
    <div class="network-row">
      <InlineMath tex="(f(x_j))_j" />
      <span class="network-arrow" aria-hidden="true"></span>
      <div class="network-block">Real-valued branch</div>
      <span class="network-arrow" aria-hidden="true"></span>
      <InlineMath tex="B(f)" />
    </div>
    <div class="network-row">
      <InlineMath tex="x" />
      <span class="network-arrow" aria-hidden="true"></span>
      <div class="network-block spiking"><strong>Spiking trunk</strong><span>Encoding → LIF → Dense</span></div>
      <span class="network-arrow" aria-hidden="true"></span>
      <InlineMath tex="T(x)" />
    </div>
    <figcaption><InlineMath tex="\widehat u(x)=B(f)^\top T(x)" /></figcaption>
  </figure>
</template>

<style scoped>
.deeponet-network{margin:0;display:grid;gap:7px;font-size:14px}
.network-row{display:grid;grid-template-columns:64px 18px minmax(0,1fr) 18px 46px;gap:6px;align-items:center;text-align:center;min-height:30px}
.network-block{background:#f1efed;padding:5px 7px;line-height:1.3}
.network-block.spiking{background:#eee8e3}
.network-block strong{font-size:14px;font-weight:600}
.network-block span{display:block;font-size:14px}
.network-arrow{position:relative;height:2px;background:#596361;margin-right:5px}
.network-arrow::after{content:"";position:absolute;right:-5px;top:-3px;border-left:7px solid #596361;border-top:4px solid transparent;border-bottom:4px solid transparent}
figcaption{text-align:center;font-size:14px;line-height:1.3;margin:0}
</style>
