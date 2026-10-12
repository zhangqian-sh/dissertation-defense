---
chapter: '8'
section: Summary
source: 'Thesis Chapter 8 · Chapter overview'
divider: chapter
---

<p class="divider-chapter">Chapter 8</p>
<div class="divider-rule" aria-hidden="true"></div>

# Summary

<!-- Bring the two independent themes together at the level of conclusions. Separate tested contributions from preliminary hybrid results and future directions. -->

---
chapter: '8'
section: Synthesis · Contributions
source: 'Thesis Chapter 8 · Synthesis of Chapters 2–7 · No experimentally
  integrated reconstruction-to-control pipeline'
---

# Contributions

<script setup>
import ContributionFigure from "/components/ContributionFigure.vue"
</script>

<div class="density summary-illustrated">
<div class="density-grid">
<div class="detail-box"><h2>Part I · Efficient neuromorphic algorithms</h2><div class="chapter-entry contribution-entry"><div><strong>Represent continuous functions with spikes</strong><p class="small">Use spike sequences to represent real-valued functions, learn solution operators, and predict evolving systems.</p></div><ContributionFigure kind="encoding" /></div><div class="chapter-entry contribution-entry"><div><strong>Convert trained networks for neuromorphic hardware</strong><p class="small">Reduce conversion error through calibration, then run scientific regression models on spiking hardware.</p></div><ContributionFigure kind="conversion" /></div><div class="chapter-entry contribution-entry"><div><strong>Train through forward computations</strong><p class="small">Estimate learning updates from forward computations, providing an alternative to backpropagation for spiking networks.</p></div><ContributionFigure kind="training" /></div></div>
<div class="detail-box"><h2>Part II · Sequence-to-sequence modeling</h2><div class="chapter-entry contribution-entry"><div><strong>Energy Transformer: reconstruct by minimizing energy</strong><p class="small">Learn an energy landscape that guides sparse measurements toward a reconstructed flow field.</p></div><ContributionFigure kind="energy" /></div><div class="chapter-entry contribution-entry"><div><strong>RFormer: reconstruct at arbitrary locations</strong><p class="small">Infer field values directly from sparse observations, without requiring a fixed computational mesh.</p></div><ContributionFigure kind="reconstruction" /></div><div class="chapter-entry contribution-entry"><div><strong>OCFormer: learn corrections to simple trajectories</strong><p class="small">Start from a tractable reference motion and learn the corrections needed to handle interacting agents and obstacles.</p></div><ContributionFigure kind="control" /></div></div>
</div>
</div>

<!--
Summarize the scientific contribution of each chapter in plain language. The two research parts remain independent studies; this page does not assert an integrated reconstruction-to-control pipeline or new quantitative results.
-->

---
chapter: '8'
section: Outlook · Hybrid Spiking RFormer
source: 'Thesis Chapter 8 · fig:summary:spiking-rformer-reconstruction;
  tab:summary:spiking-rformer · Preliminary software results'
---

# Explorary Study: Hybrid RFormer

<script setup>
import RFormerTime from "/components/RFormerTime.vue"
</script>

<div class="hybrid-rformer-layout">
<section class="hybrid-rformer-setup">
<h2>Setup</h2>
<p>Observe <InlineMath tex="(u,v,p)"/> at scattered locations. Given these measurements and new query locations, the model reconstructs the whole flow field.</p>

<h2>Which parts are spiking?</h2>
<p><strong>Spiking:</strong> signed-IF encoders after linear/GELU layers in embeddings, transformer blocks, and the output head; decoded over <InlineMath tex="T=32" /> steps.</p>
<p><strong>Real-valued:</strong> attention, normalization, and residual additions.</p>

<h2>Reconstruction accuracy</h2>
<table class="hybrid-rformer-metrics">
<thead><tr><th>Model</th><th>Relative RMSE</th></tr></thead>
<tbody>
<tr><td>ANN</td><td><InlineMath tex="0.00801\pm0.00143" /></td></tr>
<tr><td>Hybrid SNN</td><td><InlineMath tex="0.04564\pm0.00146" /></td></tr>
</tbody>
</table>
</section>
<div class="hybrid-rformer-figure">
<RFormerTime case-name="hybrid" compact />
</div>
</div>

<!--
Preliminary hybrid SpikeCalibTransformer connects the SNN conversion work to RFormer's observation/query sequence model. Read the figure left to right: physical reference, 512 sparse measurements, and decoded spiking predictions. Rows are horizontal velocity u, vertical velocity v, and pressure p, with common color limits within each row. The main alternating wake and cylinder pressure structure survive, but the SNN panels contain local artifacts. Both ANN and hybrid use identical observations, 28,668 query coordinates and reference fields across 20 test snapshots. RMSE is against physical truth, not teacher discrepancy. Signed IF responses are evaluated as decoded finite-step averages; attention matrix products, softmax, layer normalization and residual additions remain real-valued. Fine-tuning uses straight-through gradients and conventional reverse-mode optimization. This is preliminary software feasibility; hardware energy and latency benefits have not been measured for this model.
-->

---
chapter: '8'
section: Outlook · Future directions
source: 'Thesis Chapter 8 · Limitations and future directions'
---

# Future Work

<script setup>
import FutureWorkFigure from "/components/FutureWorkFigure.vue"
</script>

<div class="future-work-layout">
<div class="detail-box">
<h2>Spiking sequence-to-sequence modeling</h2>
<div class="future-work-content">
<div class="future-work-copy">
<p>Develop Spiking attention mechanism and apply them to the existing sequence-to-sequence model in SciML.</p>
</div>
<FutureWorkFigure kind="sequence" />
</div>
</div>
<div class="detail-box">
<h2>Direct Learning and Hardware Validation</h2>
<div class="future-work-content">
<div class="future-work-copy">
<p>Develop scalable direct training and on-chip learning rules. Validate accuracy, latency, and energy efficiency.</p>
</div>
<FutureWorkFigure kind="learning" />
</div>
</div>
<div class="detail-box">
<h2>Scientific Foundation Models</h2>
<div class="future-work-content">
<div class="future-work-copy">
<p>Pretraining large models across different flow fields for various downstream tasks.</p>
</div>
<FutureWorkFigure kind="foundation" />
</div>
</div>
<div class="detail-box">
<h2>Optimal Control and Reinforcement Learning</h2>
<div class="future-work-content">
<div class="future-work-copy">
<p>Extend the insights from optimal control to online planning and reinforcement learning.</p>
</div>
<FutureWorkFigure kind="control" />
</div>
</div>
</div>

<!--
Proposed future directions, not demonstrated capabilities. The dissertation motivates broader sequence mappings, direct learning, hardware validation, broader pretraining and uncertainty quantification, and feedback control. Reinforcement learning is a proposed extension.
-->

---
chapter: '8'
section: Discussion
source: 'Qian Zhang · Division of Applied Mathematics · Brown University'
cover: true
---

# Thank you.

<div class="cover-rule"></div>
<div class="author">Qian Zhang</div>
<div class="affiliation">Division of Applied Mathematics · Brown University</div>

<!-- Pause for questions and discussion. Backups follow in chapter order. -->
