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
source: 'Thesis Chapter 8 · fig:summary:spiking-rformer-reconstruction; tab:summary:spiking-rformer · Preliminary software results'
---

# Spiking RFormer recovers the main wake structures

<div style="display:grid;grid-template-columns:2.1fr 1fr;gap:26px;align-items:start;margin-top:18px"><figure class="figure"><img style="height:360px" src="/figures/ch08/spiking-rformer-reconstruction.png" alt="Hybrid Spiking RFormer at T=32: rows show u velocity, v velocity and pressure; columns show ground truth, 512 sparse observations and decoded SNN reconstruction"><figcaption>Snapshot 10 · rows: u, v, p · columns: truth, observations, SNN reconstruction.<br>Shared color limits within each row; white disk marks the cylinder.</figcaption></figure><div class="rule"><h2>Calibrated spiking responses</h2><p class="small">Signed integrate-and-fire encoders follow linear projections and GELU activations; decoded spike averages use T = 32.</p><p class="small"><strong>ANN → signed-IF calibration → end-to-end fine-tuning.</strong> Attention and normalization remain real-valued.</p><p class="small">The wake is recovered from 512 observations, with visible local artifacts.</p><p class="small"><strong>Total relative RMSE</strong><br>ANN: 0.00801 ± 0.00143<br>Hybrid SNN: 0.04564 ± 0.00146</p><p class="micro">Mean ± population SD over 20 matched snapshots. Energy and latency require hardware measurements.</p></div></div>

<!-- Preliminary hybrid SpikeCalibTransformer connects the SNN conversion work to RFormer's observation/query sequence model. Read the figure left to right: physical reference, 512 sparse measurements, and decoded spiking predictions. Rows are horizontal velocity u, vertical velocity v, and pressure p, with common color limits within each row. The main alternating wake and cylinder pressure structure survive, but the SNN panels contain local artifacts. Both ANN and hybrid use identical observations, 28,668 query coordinates and reference fields across 20 test snapshots. RMSE is against physical truth, not teacher discrepancy. Signed IF responses are evaluated as decoded finite-step averages; attention matrix products, softmax, layer normalization and residual additions remain real-valued. Fine-tuning uses straight-through gradients and conventional reverse-mode optimization. This is preliminary software feasibility; hardware energy and latency benefits have not been measured for this model. -->

---
chapter: '8'
section: Outlook · Future directions
source: 'Thesis Chapter 8 · Limitations and future directions'
---

# Toward reliable, efficient scientific inference

<div class="density">
<div class="three"><div class="detail-box"><h2>Numerical reliability</h2><p class="small"><strong>Observed limit:</strong> finite spike resolution and recursive drift; RFG accuracy worsens at larger scale.</p><p class="small"><strong>Next experiments:</strong> sweep encoding horizon and rollout length; evaluate estimator averaging at matched compute.</p><p class="small"><strong>Report:</strong> error growth, stability interval, and accuracy versus work.</p></div><div class="detail-box"><h2>Deployment evidence</h2><p class="small"><strong>Observed limit:</strong> Loihi energy excludes I/O; hybrid RFormer has software results only.</p><p class="small"><strong>Next experiments:</strong> measure complete inference energy/latency across precision and spike horizons.</p><p class="small"><strong>Report:</strong> hardware, batch/replication, I/O scope, and matched fidelity.</p></div><div class="detail-box"><h2>Generalization and constraints</h2><p class="small"><strong>Observed limit:</strong> observation shifts and unseen boundaries; M=16 amortized feasibility is 75%.</p><p class="small"><strong>Next experiments:</strong> matched reconstruction masks and boundary-shift stress tests; refine temporal clearance checks.</p><p class="small"><strong>Report:</strong> distribution, cost gap, failure fraction, and clearance.</p></div></div><p class="protocol">Future experiments, not demonstrated capabilities · retain independent reconstruction/control studies</p>
</div>

<!-- These are future directions, not additional experimental claims. -->

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
