---
chapter: '8'
section: Synthesis · Contributions
source: 'Thesis Chapter 8 · Synthesis of Chapters 2–7 · No experimentally integrated reconstruction-to-control pipeline'
---

# Computation and scientific fidelity must be co-designed

<div class="cols" style="margin-top:25px"><div class="rule"><div class="eyebrow">Part I · Neuromorphic algorithms</div><h2>Representation → conversion → training</h2><p class="small">Encoding controls resolution and operator error.</p><p class="small">Calibration supports scientific ANN-to-SNN conversion.</p><p class="small">Forward-mode training offers an alternative with an accuracy trade-off.</p></div><div class="rule teal"><div class="eyebrow">Part II · Sequence-to-sequence models</div><h2>Reconstruction and optimal control</h2><p class="small">Learned energy dynamics recover field structure.</p><p class="small">Observation/query tokens support sparse reconstruction.</p><p class="small">Trajectory maps support several control inference regimes.</p></div></div>
<div class="takeaway">The strongest conclusions pair accuracy with cost, and generalization with its tested protocol.</div>

<!-- Return to the two-theme organization from the opening. Highlight verified contributions without collapsing them into a single end-to-end system. -->

---
chapter: '8'
section: Outlook · Hybrid Spiking RFormer
source: 'Thesis Chapter 8 · fig:summary:spiking-rformer-reconstruction; tab:summary:spiking-rformer · Preliminary software results'
---

# Spiking RFormer recovers the main wake structures

<div style="display:grid;grid-template-columns:2.1fr 1fr;gap:26px;align-items:start;margin-top:18px"><figure class="figure"><img style="height:360px" src="/figures/ch08/spiking-rformer-reconstruction.png" alt="Hybrid Spiking RFormer at T=32: rows show u velocity, v velocity and pressure; columns show ground truth, 512 sparse observations and decoded SNN reconstruction"><figcaption>Snapshot 10 · rows: u, v, p · columns: truth, observations, SNN reconstruction.<br>Shared color limits within each row; white disk marks the cylinder.</figcaption></figure><div class="rule teal"><h2>Calibrated spiking responses</h2><p class="small">Signed integrate-and-fire encoders follow linear projections and GELU activations; decoded spike averages use T = 32.</p><p class="small">Attention and normalization remain real-valued. Calibration is followed by end-to-end fine-tuning.</p><p class="small">The wake is recovered from 512 observations, with visible local artifacts.</p><p class="small"><strong>Total relative RMSE</strong><br>ANN: 0.00801 ± 0.00143<br>Hybrid SNN: 0.04564 ± 0.00146</p><p class="micro">Mean ± population SD over 20 matched snapshots. Energy and latency require hardware measurements.</p></div></div>

<!-- Preliminary hybrid SpikeCalibTransformer connects the SNN conversion work to RFormer's observation/query sequence model. Read the figure left to right: physical reference, 512 sparse measurements, and decoded spiking predictions. Rows are horizontal velocity u, vertical velocity v, and pressure p, with common color limits within each row. The main alternating wake and cylinder pressure structure survive, but the SNN panels contain local artifacts. Both ANN and hybrid use identical observations, 28,668 query coordinates and reference fields across 20 test snapshots. RMSE is against physical truth, not teacher discrepancy. Signed IF responses are evaluated as decoded finite-step averages; attention matrix products, softmax, layer normalization and residual additions remain real-valued. Fine-tuning uses straight-through gradients and conventional reverse-mode optimization. This is preliminary software feasibility; hardware energy and latency benefits have not been measured for this model. -->

---
chapter: '8'
section: Outlook · Discussion
source: 'Thesis Chapter 8 · Limitations and future directions'
---

# Toward reliable, efficient scientific inference

<div class="three" style="margin-top:28px"><div class="rule"><h2>Numerical reliability</h2><p class="small">Connect representation choices to error control and long-horizon behavior.</p></div><div class="rule"><h2>Deployment evidence</h2><p class="small">Measure complete hardware costs under clearly defined precision and I/O scope.</p></div><div class="rule"><h2>Generalization and constraints</h2><p class="small">Expand observation and boundary distributions while preserving physical validity.</p></div></div>
<div style="margin-top:50px"><div class="cover-rule" style="height:3px;width:55px;background:var(--red);margin-bottom:16px"></div><p style="font-family:'Latin Modern',serif;font-size:34px;color:var(--brown)">Thank you.</p><p class="small">Qian Zhang · Brown University</p></div>

<!-- These are future directions, not additional experimental claims. Pause for discussion. Backups follow in chapter order. -->
