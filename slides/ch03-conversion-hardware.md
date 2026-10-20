---
chapter: '3'
section: Part I · Neuromorphic algorithms
source: 'Thesis Chapter 3 · Chapter overview'
divider: chapter
---

<p class="divider-chapter">Chapter 3</p>
<div class="divider-rule" aria-hidden="true"></div>

# Calibrated Conversion and Neuromorphic Deployment

<!-- Spoken transition: Inference: How to run a SciML model on efficient hardware?

Move from spike representations to converting trained scientific networks. Separate floating-point calibration accuracy from hardware precision and measured deployment costs. -->

---
chapter: '3'
section: ANN-to-SNN conversion · Calibration
source: 'Thesis Chapter 3 · sec:conversion:calibration; eq:conversion:general-bound · Floating-point conversion analysis; fig:conversion:calibration-data'
---

# ANN-to-SNN conversion and calibration

<script setup>
import CalibrationFlow from "/components/CalibrationFlow.vue"
</script>

<CalibrationFlow />

<!-- The diagram adapts the layer correspondence in data/references/flowchart/calib.png. Conversion copies affine parameters and replaces hidden activations by IF neurons. Calibration uses fixed ANN activations as targets and averaged inputs from earlier SNN layers. The inspected SNN-CAACT implementation caches these targets, optimizes the current layer weights with Adam through a clipped-floor surrogate, and proceeds layer by layer; bias correction is a separate option. The general-activation output-error bound explains why local mismatch matters, but the bound and unrelated calibration-data-size plot are omitted from this overview to keep the mechanism legible. -->

---
chapter: '3'
section: ANN-to-SNN conversion · Simulation horizon
source: 'Thesis Chapter 3 · fig:conversion:sin-horizon · Separately configured simulation horizons; fig:conversion:error-horizon'
---

# Calibration Convergence Theorem

<div class="density horizon-study">
<div class="density-grid" style="grid-template-columns:1fr 1fr;align-items:start">
<div class="detail-box calibration-theorem">
<h2>Theorem · General activations</h2>

If $f$ and $f'$ admit uniform piecewise-linear approximations and $f''$ is bounded, then the final conversion error satisfies

$$
e_n^\top H_n e_n\leq\sum_{l=1}^{n}2^{n-l+1}\,e_{c,l}^\top\left(H_l+K_l\sqrt{\mathcal L_{\mathrm{ANN}}}\,I\right)e_{c,l}.
$$

$e_l=x_l-\bar s_l$; $e_{c,l}$: local conversion mismatch.<br>
$H_l$: loss Hessian; $K_l$: derivative-dependent bound;<br>
$\mathcal L_{\mathrm{ANN}}$: ANN training loss; $n$: network depth.

</div>
<div class="three horizon-examples"><figure class="figure"><img style="height:130px" src="/figures/ch03/sin_diff_T8.png" alt="Separately configured T = 8"><figcaption style="text-align:center">

$T=8$

</figcaption></figure><figure class="figure"><img style="height:130px" src="/figures/ch03/sin_diff_T32.png" alt="Separately configured T = 32"><figcaption style="text-align:center">

$T=32$

</figcaption></figure><figure class="figure"><img style="height:130px" src="/figures/ch03/sin_diff_T128.png" alt="Separately configured T = 128"><figcaption style="text-align:center">

$T=128$

</figcaption></figure></div>
</div>
<div class="density-grid horizon-proof-row">
<div class="proof-sketch">
<h2>Proof sketch</h2>
<ol>
<li>

**Approximate the activation.** Choose piecewise-linear $\tilde f$ that uniformly approximates both $f$ and $f'$.

</li>
<li>

**Control curvature.** Expand the loss Hessian layerwise; bound the extra $f''$ terms using $K_l\sqrt{\mathcal L_{\mathrm{ANN}}}$.

</li>
<li>

**Pass to the limit.** Extend the piecewise-linear error bound to smooth activations using uniform approximation and curvature control.

</li>
</ol>
</div>
<figure class="figure"><img style="height:260px" src="/figures/ch03/error_vs_T_L2.png" alt="Separate depth-2 sweep · source widths and error axis"><figcaption style="text-align:center">Error vs. T for Different Widths</figcaption></figure>
</div>
</div>

<!-- These are the published separately configured T examples. The output-evolution slide instead inspects cumulative prefixes of one fixed T=128 conversion. -->

---
chapter: '3'
section: ANN-to-SNN conversion · Field fidelity
source: 'Thesis Chapter 3 · fig:conversion:poisson · Published matched Poisson
  comparison; tab:conversion:accuracy'
---

# Example: 2D Poisson Equation

<div class="poisson-conversion">
<div class="poisson-conversion-text">
<section class="poisson-conversion-setup">
<h2>Setup</h2>

$$
\begin{aligned}
-\Delta u&=f,\qquad x\in\Omega,\\
u|_{\partial\Omega}&=0,\qquad\Omega=[-1,1]^2.
\end{aligned}
$$

<p class="poisson-conversion-note">tanh activation · 3 hidden layers × 100 neurons.</p>
</section>
<section class="conversion-fidelity">
<h2>Calibration settings</h2>

$T=64$ spike steps · Adam, learning rate $10^{-3}$ · 5,000 updates per layer.

<h2>Results</h2>

<table><thead><tr><th>Metric</th><th>Calibrated SNN</th></tr></thead><tbody><tr><td>Relative L₂ error</td><td>0.0471</td></tr><tr><td>Spike rate</td><td>0.3727</td></tr></tbody></table>
<p class="conversion-metric-note">Error is measured against the trained ANN field. Spike rate is the fraction of nonzero spiking-layer outputs.</p>
<p class="small"><strong>Calibration restores the spatial pattern;</strong> copying weights alone gives only a coarse approximation.</p>
</section>
</div>
<div class="poisson-conversion-figures"><figure class="figure"><img style="height:200px" src="/figures/ch03/poisson_true.png" alt="Numerical reference"><figcaption>Numerical reference</figcaption></figure><figure class="figure"><img style="height:200px" src="/figures/ch03/poisson_ann.png" alt="ANN / PINN"><figcaption>ANN / PINN</figcaption></figure><figure class="figure"><img style="height:200px" src="/figures/ch03/poisson_snn_none.png" alt="SNN · weight copying"><figcaption>SNN · weight copying</figcaption></figure><figure class="figure"><img style="height:200px" src="/figures/ch03/poisson_snn_calibrated.png" alt="SNN · calibrated"><figcaption>SNN · calibrated</figcaption></figure></div>
</div>

<!--
Retain the original panels and color scales. ANN-to-reference error and SNN-to-ANN conversion error are different quantities.
-->

---
chapter: '3'
section: ANN-to-SNN conversion · Poisson spike dynamics
source: 'Archived Poisson advanced-CAA checkpoint · fixed T=64 · measured cumulative output spikes'
---

# Poisson Equation: Spiking Dynamics

<PoissonSpikeDynamics />

<!-- Same Poisson architecture and T=64 advanced-CAA protocol as the preceding example. Replay of the saved checkpoint must match the archived ANN and SNN fields before publication. Show actual cumulative means of emitted spikes, with no retraining, recalibration, or interpolated frames. Both spatial axes and all color scales stay fixed. -->

---
chapter: '3'
section: Loihi 2 · Precision
source: 'Thesis Chapter 3 · fig:loihi:precision; tab:conversion:loihi-accuracy · Source-reported RMS field error'
---

# Run the converted SNN on the hardware

<div class="fixed-point-study">
<div class="fixed-point-explanation">
<section>

## Loihi 2

An event-driven neuromorphic processor with 8-bit synaptic weights and 24-bit membrane potentials and graded spikes. Neuron updates use integer arithmetic.

## Fixed-point precision

Represent $q$ by an integer $\bar q=\lfloor 2^p q\rfloor$; decode $\hat q=2^{-p}\bar q$. A shared exponent $p$ sets the resolution and range. This maps the floating-point SNN to Loihi 2’s integer arithmetic.

## Difficulty

Finer resolution reduces the available range, risking overflow. Rounding and scale mismatches add errors beyond floating-point calibration.

</section>
<section>

## Match scales layer by layer

Choose layerwise power-of-two scales offline. For $y=Wx+b$, use bit shifts to align the integer products and bias:

$$
\bar y=\bar W\bar x\,2^{p_y-p_x-p_W}+\bar b\,2^{p_y-p_b}.
$$

Scale the spike outputs and thresholds consistently between layers.

## Increase effective weight precision

Two 8-bit connections carry the high and low bytes: **effective 16-bit weights** at **twice the synaptic cost**. Potentials and spikes remain 24-bit.

</section>
</div>
<div class="fixed-point-fields">
<figure class="figure"><img src="/figures/ch03/loihi_precision_reference.png" alt="Reference Poisson field"><figcaption>Reference</figcaption></figure>
<figure class="figure"><img src="/figures/ch03/loihi_precision_cpu.png" alt="Floating-point spiking PINN field"><figcaption>Floating-point SNN<span class="fixed-point-rms">RMS: 0.0131</span></figcaption></figure>
<figure class="figure"><img src="/figures/ch03/loihi_precision_8bit.png" alt="Loihi 2 Poisson field with 8-bit weights"><figcaption>Loihi 2 · 8-bit<span class="fixed-point-rms">RMS: 0.0215</span></figcaption></figure>
<figure class="figure"><img src="/figures/ch03/loihi_precision_16bit.png" alt="Loihi 2 Poisson field with effective 16-bit weights"><figcaption>Loihi 2 · 16-bit<span class="fixed-point-rms">RMS: 0.0160</span></figcaption></figure>
</div>
</div>

<!-- Fixed-point mapping and RMS values follow thesis Chapter 3. The four panels are crops of the original source figure; field values and colors are unchanged. RMS against the Poisson reference is not relative L2. -->

---
chapter: '3'
section: Loihi 2 · Measured scaling
source: 'Thesis Chapter 3 · fig:loihi:throughput; fig:loihi:epi; fig:loihi:edp · Measurement scope excludes I/O'
---

# Batching through replication

<div class="density">
<p style="font-size:14px; margin:0 0 16px">Each hardware SNN copy processes one input at a time (effectively batch size 1). Parallel network copies process separate inputs concurrently, acting like batching and potentially reducing energy per inference.</p>
<div class="three"><figure class="figure"><img style="height:265px" src="/figures/ch03/loihi_throughput.png" alt="Throughput · both precisions"><figcaption>Throughput · both precisions</figcaption></figure><figure class="figure"><img style="height:265px" src="/figures/ch03/loihi_epi.png" alt="Energy per inference"><figcaption>Energy per inference</figcaption></figure><figure class="figure"><img style="height:265px" src="/figures/ch03/loihi_edp.png" alt="Energy–delay product"><figcaption>Energy–delay product</figcaption></figure></div>
<div class="math-panel replication-metrics">

$$
\mathrm{throughput}=\frac{N_{\mathrm{inferences}}}{\Delta t},\quad \mathrm{EPI}=\frac{E_{\mathrm{measured}}}{N_{\mathrm{inferences}}},\quad \mathrm{EDP}=\mathrm{EPI}\times\mathrm{delay}
$$

</div>
</div>

<!-- These are measured source curves, not extrapolated CPU-versus-Loihi energy claims. No CPU energy multiplier is available. -->
