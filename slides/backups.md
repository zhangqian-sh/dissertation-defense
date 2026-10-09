---
chapter: '2'
section: Backup · Spiking marching scheme
source: 'Thesis Chapter 2 · fig:snn:ode-lorenz · Source encoder protocols and horizons'
---

# Encoder-dependent behavior on the Lorenz system

<div class="three" style="margin-top:12px"><figure class="figure tall"><img src="/figures/ch02/ode_lorenz_error.png" alt="Lorenz lower triangular cascade error"><figcaption>Lower triangular · K=1000</figcaption></figure><figure class="figure tall"><img src="/figures/ch02/ode_lorenz_error_rate.png" alt="Lorenz rate encoding cascade error"><figcaption>Rate · K=100</figcaption></figure><figure class="figure tall"><img src="/figures/ch02/ode_lorenz_error_float32.png" alt="Lorenz float encoding cascade error"><figcaption>Floating point · source protocol</figcaption></figure></div>

<div class="protocol">

$\dot x=\sigma(y-x),\ \dot y=x(\rho-z)-y,\ \dot z=xy-\beta z$ · source encoder/horizon protocols differ; error curves are not an equal-budget comparison.

</div>

<!-- Different horizons are explicit. These are source results, not alternate states of the heat interaction. -->

---
chapter: '3'
section: Backup · Conversion horizon
source: 'Thesis Chapter 3 · fig:conversion:error-horizon · Source depth and horizon sweep'
---

# Conversion error depends on depth and horizon

<div class="three" style="margin-top:12px"><figure class="figure tall"><img src="/figures/ch03/error_vs_T_L2.png" alt="Conversion error versus T at depth2"><figcaption>Depth L=2</figcaption></figure><figure class="figure tall"><img src="/figures/ch03/error_vs_T_L3.png" alt="Conversion error versus T at depth3"><figcaption>Depth L=3</figcaption></figure><figure class="figure tall"><img src="/figures/ch03/error_vs_T_L4.png" alt="Conversion error versus T at depth4"><figcaption>Depth L=4</figcaption></figure></div>

<div class="protocol">

General-activation bound requires bounded curvature and approximable values/first derivatives. Depth weight $2^{L-l+1}$ amplifies early mismatch; finite T converges toward a calibration/ANN error floor.

</div>

<!-- Use original axis definitions. Do not read this as a universal asymptotic convergence rate. -->

---
chapter: '4'
section: Backup · Forward-gradient definitions
source: 'Thesis Chapter 4 · tab:rfg:methods; tab:rfg:poisson'
---

# Surrogate choice and gradient estimator are separate

<div class="density">
<table><thead><tr><th>Configuration</th><th>Test MSE</th><th>Relative L₂</th></tr></thead><tbody><tr><td>SG · BP</td><td>1.89 × 10⁻⁴</td><td>0.0419</td></tr><tr><td>WSG · BP</td><td>2.05 × 10⁻⁴</td><td>0.0394</td></tr><tr><td>SG · global RFG</td><td>2.12 × 10⁻⁴</td><td>0.0642</td></tr><tr><td>WSG · global RFG</td><td>3.29 × 10⁻⁴</td><td>0.0637</td></tr><tr><td>SG · layerwise RFG</td><td>2.09 × 10⁻⁴</td><td>0.0583</td></tr><tr><td>WSG · layerwise RFG</td><td>2.08 × 10⁻⁴</td><td>0.0580</td></tr></tbody></table>

<div class="density-grid ">
<div class="detail-box"><h2>Standard surrogate</h2>
<div class="math-panel">

$$
f_{SG}^{\prime}(a)=\frac{e^{-a^2/(2\sigma^2)}}{\sigma\sqrt{2\pi}}
$$

</div>
</div>
<div class="detail-box"><h2>Weak surrogate</h2>
<div class="math-panel">

$$
f_{WSG}^{\prime}(a)=\frac1{K_s}\sum_j\frac{\delta_j}{\sigma^2}[H(a+\delta_j)-H(a)]
$$

</div>
</div>
</div><p class="protocol">a = U − Uth · δⱼ ∼ N(0,σ²) shifts thresholds; Bernoulli parameter directions define RFG · global/layerwise is a separate choice.</p>

<!-- SG is the standard surrogate, WSG the weak surrogate. RFG directions and threshold noise are separate sources of randomness. -->

</div>

---
chapter: '5'
section: Backup · Energy Transformer ablations
source: 'Thesis Appendix B · tab:app-et-temporal; tab:app-et-module · Source test relative errors'
---

# Training coverage and module choice matter

<div class="cols" style="margin-top:12px"><div><h2>Temporal training coverage · vortex</h2><table><thead><tr><th>Coverage</th><th>Velocity</th><th>Pressure</th></tr></thead><tbody><tr><td>100%</td><td>0.0405</td><td>0.0798</td></tr><tr><td>75%</td><td>0.0494</td><td>0.1220</td></tr><tr><td>50%</td><td>0.0595</td><td>0.1526</td></tr><tr><td>25%</td><td>0.1616</td><td>0.3116</td></tr></tbody></table><p class="micro">Separately trained configurations; unchanged spatial masking.</p></div><div><h2>Module ablation · 3D jet</h2><table><thead><tr><th>Module</th><th>Velocity</th><th>Pressure</th></tr></thead><tbody><tr><td>Energy MHA</td><td>0.4671</td><td>0.1784</td></tr><tr><td>Hopfield</td><td>0.4213</td><td>0.1928</td></tr><tr><td>Full ET</td><td>0.4421</td><td>0.1785</td></tr></tbody></table><p class="micro">Full ET does not minimize every field error. Read alongside spectra.</p></div></div>

<p class="protocol">Temporal ablation: fewer training snapshots weaken mode coverage. Module ablation: channel-specific errors expose trade-offs; neither attention nor Hopfield alone dominates both channels.</p>

<!-- Temporal coverage is not an inference-context or spatial-mask control. -->

---
chapter: '5'
section: Backup · Energy Transformer inference cost
source: 'Thesis Chapter 5 · tab:et:timing · Single NVIDIA A6000; 12 inference iterations; tab:app-et-module'
---

# Separate offline training from iterative inference

<div class="density">
<div class="density-grid ">
<div class="detail-box"><h2>Timing · source benchmarks</h2><table><thead><tr><th>Benchmark</th><th>Training</th><th>Per snapshot</th></tr></thead><tbody><tr><td>Vortex street</td><td>≈ 90 min</td><td>≈ 2.7 ms</td></tr><tr><td>Schlieren jet</td><td>≈ 150 min</td><td>≈ 2.5 ms</td></tr><tr><td>3D jet</td><td>≈ 70 min</td><td>≈ 100 ms</td></tr></tbody></table><p class="small">Train a reusable energy offline; each new snapshot requires 12 token updates.</p></div>
<div class="detail-box"><h2>Module ablation · 3D jet</h2><table><thead><tr><th>Module</th><th>Velocity</th><th>Pressure</th></tr></thead><tbody><tr><td>Energy MHA</td><td>0.4671</td><td>0.1784</td></tr><tr><td>Hopfield</td><td>0.4213</td><td>0.1928</td></tr><tr><td>Full ET</td><td>0.4421</td><td>0.1785</td></tr></tbody></table><p class="small">Full model balances the two channels; it does not minimize every pointwise metric.</p></div>
</div>
<div class="math-panel">

$$
\mathrm{inference\ work}\ \propto\ N_{iter}\times\mathrm{energy\ gradient\ evaluation}
$$

</div>
<p class="protocol">Timing: single NVIDIA A6000 · ablation: separate source relative-error table · distribution and masking coverage bound reuse</p>
</div>

<!-- Times are source measurements with the stated hardware and iteration count. These are not performance measurements of the presentation or a matched comparison with RFormer. -->
>

---
chapter: '6'
section: Backup · RFormer baselines
source: 'Thesis Chapter 6 · tab:rformer:vortex · Total test relative RMSE, mean ± standard deviation'
---

# Vortex-street baseline comparison

<table style="margin-top:15px;font-size:16px"><thead><tr><th>Method</th><th>Total relative RMSE</th></tr></thead><tbody><tr class="highlight"><td>RFormer</td><td>0.0080 ± 0.0014</td></tr><tr><td>Voronoi CNN</td><td>0.0184 ± 0.0008</td></tr><tr><td>Gappy POD</td><td>0.0338 ± 0.0028</td></tr><tr><td>CNP</td><td>0.1620 ± 0.0056</td></tr><tr><td>ANP</td><td>0.1709 ± 0.0046</td></tr><tr><td>Interpolation</td><td>0.1843 ± 0.0004</td></tr><tr><td>TNP</td><td>0.3082 ± 0.0100</td></tr><tr><td>Kriging</td><td>0.6243 ± 0.0012</td></tr></tbody></table>

<div class="protocol">

Metric: $\sqrt{\sum\|\hat v-v\|^2}/\sqrt{\sum\|v\|^2}$ · total test relative RMSE · mean ± source SD across snapshots · source vortex observation protocol.

</div>

<!-- Source dataset and observation protocol apply. The ranking is not transferred to blood flow or weather. -->

---
chapter: '7'
section: Backup · OCFormer inference regimes
source: 'Thesis Chapter 7 · tab:oc:regimes · Protocol-specific timing, not a single universal latency'
---

# Three regimes answer different deployment questions

<div class="density">
<table><thead><tr><th>Regime</th><th>Online work</th><th>Boundary coverage</th></tr></thead><tbody><tr><td>Per-instance</td><td>≈20 min optimization</td><td>One fixed pair</td></tr><tr><td>Transfer</td><td>Seconds of adaptation</td><td>Structured / small perturbations</td></tr><tr><td>Amortized</td><td>≈220 ms forward pass</td><td>Held-out in-distribution pairs</td></tr></tbody></table><div class="three"><div class="detail-box"><h2>Per-instance</h2><p class="small">New pair → initialize model → Adam/L-BFGS → trajectory</p><p class="small">Physics losses fit one latent curve.</p></div><div class="detail-box"><h2>Transfer</h2><p class="small">Trained model → changed pair → fine-tune → trajectory</p><p class="small">Freeze the trained backbone; adapt wrapper maps with L-BFGS.</p></div><div class="detail-box"><h2>Amortized</h2><p class="small">Many pairs offline → fixed model → new pair → trajectory</p><p class="small">No online weight updates within the tested distribution.</p></div></div><p class="protocol">Protocol-specific source timings · per-instance 3D examples do not inherit amortized 2D latency · transfer depends on perturbation size</p>
</div>

<!-- Timing is reproduced from the source protocol. The collection/export job times are unrelated to inference performance. -->

---
chapter: '7'
section: Backup · OCFormer amortized generalization
source: 'Thesis Chapter 7 · tab:oc:amortized · 100 rotated training pairs; JIT forward-pass timing over 100 runs'
---

# Fast inference does not guarantee feasibility

<div class="density">
<p class="protocol">Held-out rotations of 2D antipodal configurations · 100 rotated training pairs · JIT timing over 100 runs</p><table><thead><tr><th>M</th><th>Test cost</th><th>LB gap</th><th>Feasible</th><th>Inference</th></tr></thead><tbody><tr><td>8</td><td>0.4053</td><td>1.3%</td><td>100%</td><td>218.6 ± 1.3 ms</td></tr><tr><td>16</td><td>0.8399</td><td>5.0%</td><td>75%</td><td>220.9 ± 1.2 ms</td></tr></tbody></table><div class="density-grid ">
<div class="detail-box"><h2>Cost relative to free motion</h2>
<div class="math-panel">

$$
J_{LB}=\sum_i\frac{\|x_i^T-x_i^0\|^2}{2T},\quad \mathrm{gap}=\frac{J-J_{LB}}{J_{LB}}
$$

</div>
<p class="small">Lower bound omits collisions; the gap is not against the unknown constrained optimum.</p></div>
<div class="detail-box"><h2>Sampled feasibility</h2>
<div class="math-panel">

$$
c_{min}=\min_{i<j,t_k}(\|x_i(t_k)-x_j(t_k)\|-2r)
$$

</div>
<p class="small">Feasible fraction: held-out boundary pairs with positive minimum clearance. At M = 16, one quarter fails this test.</p></div>
</div><p class="protocol">Demonstrated: zero-shot rotated pairs · open: arbitrary boundaries, variable M, amortized 3D · timing ± source SD</p>
</div>

<!-- Feasibility is the fraction of held-out pairs with positive minimum inter-agent clearance. Keep the lower-bound denominator explicit. Full cost uncertainty is retained in the thesis table and backup provenance. -->
