<script setup lang="ts">
import katex from 'katex'
const math = (tex: string) => katex.renderToString(tex, { throwOnError: true })
const positions = [80, 220, 360]
</script>
<template>
<div class="rfg-directions">
  <section>
    <h2>Global direction</h2>
    <div class="direction-diagram">
      <svg viewBox="0 0 530 174" aria-hidden="true">
        <path d="M30 87 H55 V48 H74 M55 87 V126 H74" class="shaft"/>
        <g v-for="y in [48,126]" :key="y">
          <path :d="`M174 ${y} H214 M314 ${y} H354 M454 ${y} H490`" class="shaft"/>
          <polygon v-for="x in [80,220,360,496]" :key="x" :points="`${x},${y} ${x-8},${y-3.5} ${x-8},${y+3.5}`" class="head"/>
        </g>
      </svg>
      <span class="diagram-input" v-html="math('x')"/>
      <template v-for="(x,i) in positions" :key="i">
        <div class="parameter-node original-node" :style="{left:x/5.3+'%'}" v-html="math(String.raw`\theta_${i+1}`)"/>
        <div class="parameter-node perturbed-node" :style="{left:x/5.3+'%'}" v-html="math(String.raw`\theta_${i+1}+\epsilon v_${i+1}`)"/>
      </template>
      <span class="diagram-output original-output" v-html="math('y_0')"/>
      <span class="diagram-output perturbed-output" v-html="math('y_v')"/>
    </div>
    <div class="gradient-estimate" v-html="math(String.raw`d_v=\mathrm{JVP}_\theta(\mathcal L;v),\qquad\hat g=d_vv`)"/>
  </section>
  <section>
    <h2>Layerwise direction</h2>
    <div class="direction-diagram">
      <svg viewBox="0 0 530 174" aria-hidden="true">
        <path d="M30 87 H74 M174 87 H195 V48 H214 M195 87 V126 H214 M314 48 H337 V87 H354 M314 126 H337 V87 M454 87 H473 V48 H490 M473 87 V126 H490" class="shaft"/>
        <polygon v-for="point in [[80,87],[220,48],[220,126],[360,87],[496,48],[496,126]]" :key="point.join('-')" :points="`${point[0]},${point[1]} ${point[0]-8},${point[1]-3.5} ${point[0]-8},${point[1]+3.5}`" class="head"/>
      </svg>
      <span class="diagram-input" v-html="math('x')"/>
      <div class="parameter-node shared-node" style="left:15.094%"><span v-html="math(String.raw`\theta_1`)"/><span class="shared-label">Shared weights</span></div>
      <div class="parameter-node original-node" style="left:41.509%" v-html="math(String.raw`\theta_2`)"/>
      <div class="parameter-node perturbed-node" style="left:41.509%" v-html="math(String.raw`\theta_2+\epsilon v_2`)"/>
      <div class="parameter-node shared-node" style="left:67.925%"><span v-html="math(String.raw`\theta_3`)"/><span class="shared-label">Shared weights</span></div>
      <span class="diagram-output original-output" v-html="math('y_0')"/>
      <span class="diagram-output perturbed-output" v-html="math('y_v')"/>
    </div>
    <div class="gradient-estimate" v-html="math(String.raw`d_{v_2}=\mathrm{JVP}_{\theta_2}(\mathcal L;v_2),\qquad\hat g^2=d_{v_2}v_2`)"/>
  </section>
</div>
</template>
<style scoped>
.rfg-directions{display:grid;grid-template-columns:1fr 1fr;gap:28px;font-size:14px}.rfg-directions section{min-width:0}.rfg-directions h2{font-size:16px;margin:0 0 4px}.direction-diagram{position:relative;height:174px}.direction-diagram>svg{position:absolute;inset:0;width:100%;height:174px}.shaft{fill:none;stroke:#596361;stroke-width:1.6}.head{fill:#596361}.parameter-node{position:absolute;width:17.736%;height:48px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;border:1px solid #98a4ae;font-size:16px;background:white}.original-node{top:24px}.perturbed-node{top:102px;background:#f1f2f2}.shared-node{top:63px}.shared-label{font-size:12px;color:#596361;white-space:nowrap}.diagram-input,.diagram-output{position:absolute;font-size:16px;transform:translateY(-50%)}.diagram-input{left:1%;top:87px}.diagram-output{left:94.5%}.original-output{top:48px}.perturbed-output{top:126px}.rfg-directions p{font-size:14px;line-height:1.45;margin:0 0 8px}.gradient-estimate{font-size:16px;text-align:center;padding:7px 0;border-top:1px solid #dce1df}
</style>
