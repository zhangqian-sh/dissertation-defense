<script setup lang="ts">
import katex from 'katex'
const math = (tex:string) => katex.renderToString(tex, {throwOnError:false})
const fields = [
  {x:24,y:46,w:134,h:68,a:.9},
  {x:24,y:167,w:134,h:68,a:.75},
  {x:490,y:122,w:116,h:78,a:.62},
]
</script>
<template>
  <div class="sms-method-diagram" role="img" aria-label="Initial states are encoded once. Two binary spike histories feed the trained network. Thresholded output spikes return to the history for recursive marching; decoding is performed for the saved output trajectory.">
    <svg viewBox="0 0 620 300">
      <g v-for="(f,i) in fields" :key="i">
        <path :d="`M${f.x} ${f.y} V${f.y+f.h} H${f.x+f.w}`" fill="none" stroke="#98a4ae" stroke-width="1" />
        <g v-for="j in 16" :key="j">
          <rect v-for="k in 8" :key="k" :x="f.x+(j-1)*f.w/16" :y="f.y+f.h-k*f.h/8" :width="f.w/16-.8" :height="f.h/8-.8" :fill="k<=Math.floor(8*f.a*Math.sin(Math.PI*(j-1)/15))?'#315d79':'#eeedeb'" />
        </g>
      </g>
      <path d="M158 80 H174 V201 H158 M174 141 H219" fill="none" stroke="#596361" stroke-width="1.4" />
      <polygon points="225,141 217,137.5 217,144.5" fill="#596361" />
      <rect x="225" y="91" width="236" height="106" fill="#f1f2f2" />
      <g v-for="(layer,i) in ['LIF','Dense','Dense']" :key="i">
        <rect :x="237+i*78" y="117" width="56" height="49" fill="white" stroke="#98a4ae" stroke-width=".8" />
        <text :x="265+i*78" y="147" text-anchor="middle" class="layer">{{layer}}</text>
        <path v-if="i<2" :d="`M${293+i*78} 141 H${309+i*78}`" stroke="#596361" stroke-width="1.4" />
        <polygon v-if="i<2" :points="`${315+i*78},141 ${307+i*78},137.5 ${307+i*78},144.5`" fill="#596361" />
      </g>
      <text x="343" y="215" text-anchor="middle">Hidden width 500</text>
      <path d="M461 141 H484" stroke="#596361" stroke-width="1.4" />
      <polygon points="490,141 482,137.5 482,144.5" fill="#596361" />
      <path d="M606 161 H616 V284 H8 V201 H18" fill="none" stroke="#596361" stroke-width="1.4" />
      <polygon points="24,201 16,197.5 16,204.5" fill="#596361" />
    </svg>
    <div class="sms-field-label history-old" v-html="math('\\hat s^{n-1}')"></div>
    <div class="sms-field-label history-current" v-html="math('\\hat s^n')"></div>
    <div class="sms-field-label next-state" v-html="math('\\hat s^{n+1}')"></div>
  </div>
</template>
<style scoped>
.sms-method-diagram{position:relative;width:92%;margin:0 auto}
svg{display:block;width:100%;height:auto}svg text{font-family:'Noto Serif',serif;fill:#596361;font-size:16px}
svg .operation{fill:#232727;font-size:13px}svg .layer{fill:#232727;font-size:16px}svg .feedback-label{fill:#315d79;font-size:15px}
.sms-field-label{position:absolute;font-size:16px;text-align:center;transform:translateX(-50%)}
.history-old{left:14.7%;top:39%}.history-current{left:14.7%;top:79.3%}.next-state{left:88.4%;top:68%}.network{left:55.3%;top:20%}
</style>
