---
chapter: '3'
section: Chapter 3 · Transition
source: 'Thesis Chapter 3 · Chapter overview'
divider: chapter
---

<div class="eyebrow">Chapter 3</div>
<div class="divider-rule" aria-hidden="true"></div>

# ANN-to-SNN conversion and hardware

<p class="lead">How can scientific predictions survive conversion and hardware deployment?</p>

<!-- Move from spike representations to converting trained scientific networks. Separate floating-point calibration accuracy from hardware precision and measured deployment costs. -->

---
chapter: '3'
section: ANN-to-SNN conversion · Calibration
source: 'Thesis Chapter 3 · sec:conversion:calibration; eq:conversion:general-bound · Floating-point conversion analysis'
---

# Calibrate the local mismatch before it propagates

<p class="subtitle">Scientific regression uses smooth activations whose curvature matters in conversion.</p>
<div class="flow"><div><strong>Train the ANN</strong><br><span class="small">Fit the scientific task with smooth activations.</span></div><span class="arrow">→</span><div><strong>Replace activations</strong><br><span class="small">Use integrate-and-fire neurons at a configured T.</span></div><span class="arrow">→</span><div><strong>Calibrate layer by layer</strong><br><span class="small">Reduce local mismatch through weights and biases.</span></div></div>
<div class="cols" style="margin-top:30px"><div class="rule"><h2>Why calibration helps</h2><p class="small">The error bound links final-output error to local conversion mismatch, layerwise amplification, and ANN training loss.</p></div><div class="rule"><h2>What the result does not cover</h2><p class="small">The floating-point analysis does not remove fixed-point rounding error or guarantee hardware energy savings.</p></div></div>

<!-- The thesis extends the ReLU-specific argument to activations with approximable values/first derivatives and bounded second derivatives. Explain the bound qualitatively rather than presenting it as an exact prediction of measured error. -->

---
chapter: '3'
section: ANN-to-SNN conversion · Field fidelity
source: 'Thesis Chapter 3 · fig:conversion:poisson · Published matched Poisson comparison'
---

# Calibration restores the spatial solution

<p class="subtitle">Reference, ANN, uncalibrated SNN, and calibrated SNN shown together.</p>
<div class="four" style="margin-top:25px">
<figure class="figure"><img src="/figures/ch03/poisson_true.png" alt="Poisson numerical reference"><figcaption>Numerical reference</figcaption></figure>
<figure class="figure"><img src="/figures/ch03/poisson_ann.png" alt="Poisson ANN prediction"><figcaption>ANN</figcaption></figure>
<figure class="figure"><img src="/figures/ch03/poisson_snn_none.png" alt="Poisson uncalibrated SNN"><figcaption>SNN · no calibration</figcaption></figure>
<figure class="figure"><img src="/figures/ch03/poisson_snn_calibrated.png" alt="Poisson calibrated SNN"><figcaption>SNN · calibrated</figcaption></figure>
</div>
<div class="takeaway">Weight copying alone can distort a regression field; post-training calibration targets that mismatch.</div>

<!-- Retain the original panels and color scales. ANN-to-reference error and SNN-to-ANN conversion error are different quantities. -->

---
chapter: '3'
section: ANN-to-SNN conversion · Simulation horizon
source: 'Thesis Chapter 3 · fig:conversion:sin-horizon · Separately configured simulation horizons'
---

# More spike steps refine the approximation

<div class="three" style="margin-top:24px">
<figure class="figure"><img src="/figures/ch03/sin_diff_T8.png" alt="Sine conversion with T8"><figcaption>T = 8</figcaption></figure>
<figure class="figure"><img src="/figures/ch03/sin_diff_T32.png" alt="Sine conversion with T32"><figcaption>T = 32</figcaption></figure>
<figure class="figure"><img src="/figures/ch03/sin_diff_T128.png" alt="Sine conversion with T128"><figcaption>T = 128</figcaption></figure>
</div>
<div class="takeaway">Increasing T trades simulation cost for resolution; residual ANN and calibration errors set an accuracy floor.</div>

<!-- These are the published separately configured T examples. The next slide instead inspects cumulative prefixes of one fixed T=64 conversion. -->

---
chapter: '3'
section: ANN-to-SNN conversion · Output evolution
source: 'Burgers PINN · matched original ANN checkpoint · fresh advanced CAA at horizon 128 · all emitted prefixes captured'
---

# Burgers: reference, SNN and difference across T

<ConversionOverT />

<!-- Demo: start at prefix 1 and play to show the full buildup; scrub to 65, 80, 96 and 128 to inspect later prefixes. Each field is a captured cumulative mean of actual emitted final-layer spikes from one SNN calibrated at fixed horizon 128. Weights, thresholds and initialization remain fixed. This is a fresh calibration of the ANN checkpoint whose grid predictions match the archive, not reproduction of the historical calibrated SNN. No interpolation or per-prefix recalibration. The reference [t,x] layout is restored and checked against initial/boundary conditions. -->

---
chapter: '3'
section: Loihi 2 · Precision
source: 'Thesis Chapter 3 · fig:loihi:precision; tab:conversion:loihi-accuracy · Source-reported RMS field error'
---

# Fixed-point precision adds a distinct error source

<div class="cols wide-left" style="margin-top:20px">
<figure class="figure tall"><img src="/figures/ch03/loihi_precision_results.png" alt="Poisson field comparison across CPU and Loihi precision"><figcaption>Published field comparison on the source Poisson benchmark.</figcaption></figure>
<div><table><thead><tr><th>Platform / precision</th><th>RMS error</th></tr></thead><tbody><tr><td>CPU</td><td>0.0131</td></tr><tr><td>Loihi · 8-bit</td><td>0.0215</td></tr><tr><td>Loihi · effective 16-bit</td><td>0.0160</td></tr></tbody></table><p class="small" style="margin-top:20px">Effective 16-bit precision uses two 8-bit connections per weight.</p><p class="micro">Reported as RMS in the thesis. Physical units and normalization are not independently recovered; these are not relabeled relative L₂ errors.</p></div>
</div>

<!-- Keep the source metric terminology. Do not compare these numbers with the relative L2 values from other chapters. -->

---
chapter: '3'
section: Loihi 2 · Measured scaling
source: 'Thesis Chapter 3 · fig:loihi:throughput; fig:loihi:epi; fig:loihi:edp · Measurement scope excludes I/O'
---

# Replication changes throughput and energy cost

<div class="three" style="margin-top:25px">
<figure class="figure"><img src="/figures/ch03/loihi_throughput.png" alt="Measured Loihi throughput versus replicas for both precisions"><figcaption>Throughput versus parallel replicas</figcaption></figure>
<figure class="figure"><img src="/figures/ch03/loihi_epi.png" alt="Measured Loihi energy per inference versus replicas"><figcaption>Energy per inference</figcaption></figure>
<figure class="figure"><img src="/figures/ch03/loihi_edp.png" alt="Measured Loihi energy delay product versus replicas"><figcaption>Energy–delay product</figcaption></figure>
</div>
<div class="takeaway">Keep both precision curves visible. The reported transition near 70 replicas involves multiple chips; energy excludes I/O.</div>

<!-- These are measured source curves, not extrapolated CPU-versus-Loihi energy claims. No CPU energy multiplier is available. -->
