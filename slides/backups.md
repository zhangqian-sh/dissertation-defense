---
appendix: index
routeAlias: appendix-index
section: Appendix
---

# Appendix

<div class="appendix-content appendix-index-grid">
<section class="detail-box">
<h2>Part I · Efficient neuromorphic algorithms</h2>
<Link to="/appendix-lorenz" class="appendix-entry"><span>A1</span><div><strong>Spiking representations</strong><p>Lorenz system: encoding and rollout behavior.</p></div></Link>
<Link to="/appendix-conversion" class="appendix-entry"><span>A2</span><div><strong>Conversion and calibration</strong><p>Conversion error across network depths and spike horizons.</p></div></Link>
<Link to="/appendix-poisson" class="appendix-entry"><span>A3</span><div><strong>Direct SNN training</strong><p>Poisson results: SG/WSG and gradient estimators.</p></div></Link>
</section>
<section class="detail-box">
<h2>Part II · Sequence-to-sequence modeling</h2>
<Link to="/appendix-et-ablations" class="appendix-entry"><span>A4</span><div><strong>Energy Transformer · ablations</strong><p>Temporal training coverage and energy modules.</p></div></Link>
<Link to="/appendix-et-cost" class="appendix-entry"><span>A5</span><div><strong>Energy Transformer · computational cost</strong><p>Offline training and iterative reconstruction.</p></div></Link>
<Link to="/appendix-rformer" class="appendix-entry"><span>A6</span><div><strong>RFormer · baseline comparison</strong><p>Vortex-street reconstruction accuracy.</p></div></Link>
<Link to="/appendix-oc-regimes" class="appendix-entry"><span>A7</span><div><strong>OCFormer · deployment regimes</strong><p>Per-instance optimization, transfer, and amortization.</p></div></Link>
<Link to="/appendix-oc-generalization" class="appendix-entry"><span>A8</span><div><strong>OCFormer · amortized generalization</strong><p>Cost, inference time, and sampled feasibility.</p></div></Link>
</section>
</div>

<!-- Click an entry to open a backup; its footer returns to this index. Content remains in dissertation chapter order. -->

---
chapter: '2'
appendix: A1
routeAlias: appendix-lorenz
section: Backup · Spiking marching scheme
source: 'Thesis Chapter 2 · fig:snn:ode-lorenz · Source encoder protocols and horizons'
---

# Example: Lorenz System

<div class="appendix-content">
<div class="appendix-equation">

$\dot x=\sigma(y-x),\qquad \dot y=x(\rho-z)-y,\qquad \dot z=xy-\beta z.$

</div>
<p>Compare teacher-forced and autoregressive predictions within each encoder's recorded rollout.</p>
<div class="appendix-plots">
<figure><img src="/figures/ch02/ode_lorenz_error.png" alt="Lorenz error: teacher-forced and autoregressive predictions using Ours at K=1000"><figcaption>Ours · <InlineMath tex="K=1000" /></figcaption></figure>
<figure><img src="/figures/ch02/ode_lorenz_error_rate.png" alt="Lorenz error: teacher-forced and autoregressive predictions using Rate at K=100"><figcaption>Rate · <InlineMath tex="K=100" /></figcaption></figure>
<figure><img src="/figures/ch02/ode_lorenz_error_float32.png" alt="Lorenz error: teacher-forced and autoregressive predictions using the floating-point source protocol"><figcaption>Floating point · source protocol</figcaption></figure>
</div>
<p>Original plot legends: “Non Cascade Pred” denotes teacher-forced prediction; “Cascade Pred” denotes autoregressive prediction.</p>
<p>The encoding horizons and source protocols differ. These curves are not an equal-budget ranking of encoders.</p>
</div>

<!-- Original curves, axes, and horizons retained. Ours is the source lower-triangular encoding. Do not treat these as alternate states of the heat interaction. -->

---
chapter: '3'
appendix: A2
routeAlias: appendix-conversion
section: Backup · Conversion horizon
source: 'Thesis Chapter 3 · fig:conversion:error-horizon · Source depth and horizon sweep'
---

# Conversion Error: Depth and Spike Horizon

<div class="appendix-content">
<p>Each panel fixes depth <InlineMath tex="L" /> and varies width and spike horizon <InlineMath tex="T" />. Legend entries give depth × hidden width.</p>
<div class="appendix-plots appendix-conversion-plots">
<figure><img src="/figures/ch03/error_vs_T_L2.png" alt="Conversion error versus spike horizon at depth L=2"><figcaption>Depth <InlineMath tex="L=2" /></figcaption></figure>
<figure><img src="/figures/ch03/error_vs_T_L3.png" alt="Conversion error versus spike horizon at depth L=3"><figcaption>Depth <InlineMath tex="L=3" /></figcaption></figure>
<figure><img src="/figures/ch03/error_vs_T_L4.png" alt="Conversion error versus spike horizon at depth L=4"><figcaption>Depth <InlineMath tex="L=4" /></figcaption></figure>
</div>
<div class="appendix-two-col">
<section><h2>Finite horizon and error floor</h2><p>The original axes are <InlineMath tex="\log_2 T" /> and <InlineMath tex="\log_2\mathrm{Error}" />. Larger horizons reduce finite-spike mismatch; the curves can level off at a calibration/ANN error floor.</p></section>
<section><h2>Connection to the theorem</h2><p>The general-activation bound assumes bounded curvature and uniform approximation of values and first derivatives. Its depth weight <InlineMath tex="2^{L-l+1}" /> amplifies early-layer mismatch.</p></section>
</div>
</div>

<!-- Original axes, widths, and measured curves retained. These empirical sweeps do not establish a universal asymptotic convergence rate. -->

---
chapter: '4'
appendix: A3
routeAlias: appendix-poisson
section: Backup · Forward-gradient definitions
source: 'Thesis Chapter 4 · tab:rfg:methods; tab:rfg:poisson'
---

# Example: 1D Poisson Equation

<div class="appendix-content appendix-poisson">
<section>
<h2>Standard surrogate · SG</h2>

$$
f_{\mathrm{SG}}'(a)=\frac{e^{-a^2/(2\sigma^2)}}{\sigma\sqrt{2\pi}}.
$$

<h2>Weak surrogate · WSG</h2>

$$
f_{\mathrm{WSG}}'(a)=\frac1{K_s}\sum_{j=1}^{K_s}\frac{\delta_j}{\sigma^2}\bigl[H(a+\delta_j)-H(a)\bigr].
$$

<p><InlineMath tex="a=U-U_{\mathrm{th}}" /> is the threshold offset and <InlineMath tex="\delta_j\sim\mathcal N(0,\sigma^2)" /> shifts the threshold.</p>
<p>Threshold sampling defines WSG. Bernoulli parameter directions define randomized forward gradients; global versus layerwise is a separate choice.</p>
</section>
<section>
<h2>Surrogate choice × gradient estimator</h2>
<table class="appendix-grouped-table"><thead><tr><th rowspan="2">Estimator</th><th colspan="2">SG</th><th colspan="2">WSG</th></tr><tr><th>Test MSE</th><th>Relative L₂</th><th>Test MSE</th><th>Relative L₂</th></tr></thead><tbody>
<tr><td>BP</td><td>1.89 × 10⁻⁴</td><td>0.0419</td><td>2.05 × 10⁻⁴</td><td>0.0394</td></tr>
<tr><td>Global</td><td>2.12 × 10⁻⁴</td><td>0.0642</td><td>3.29 × 10⁻⁴</td><td>0.0637</td></tr>
<tr><td>Layerwise</td><td>2.09 × 10⁻⁴</td><td>0.0583</td><td>2.08 × 10⁻⁴</td><td>0.0580</td></tr>
</tbody></table>
<p>Reported Poisson test results. The main presentation's six matched runs use the Darcy problem and form a separate experiment.</p>
</section>
</div>

<!-- SG/WSG surrogate definitions and source Poisson values are unchanged. Threshold noise and parameter-direction randomness are distinct. -->

---
chapter: '5'
appendix: A4
routeAlias: appendix-et-ablations
section: Backup · Energy Transformer ablations
source: 'Thesis Appendix B · tab:app-et-temporal; tab:app-et-module · Source test relative errors'
---

# Energy Transformer: Ablation Studies

<div class="appendix-content appendix-two-col">
<section class="detail-box">
<h2>Temporal training coverage · vortex street</h2>
<p>Train separate models with fewer temporal snapshots while retaining the spatial masking protocol.</p>
<table><thead><tr><th>Coverage</th><th>Velocity</th><th>Pressure</th></tr></thead><tbody>
<tr><td>100%</td><td>0.0405</td><td>0.0798</td></tr><tr><td>75%</td><td>0.0494</td><td>0.1220</td></tr><tr><td>50%</td><td>0.0595</td><td>0.1526</td></tr><tr><td>25%</td><td>0.1616</td><td>0.3116</td></tr>
</tbody></table>
<p>Reduced temporal coverage increases the reported test errors, especially for pressure. This changes training coverage, not inference context.</p>
</section>
<section class="detail-box">
<h2>Energy modules · 3D jet</h2>
<p>Compare attention energy alone, Hopfield energy alone, and the full Energy Transformer.</p>
<table><thead><tr><th>Module</th><th>Velocity</th><th>Pressure</th></tr></thead><tbody>
<tr><td>Energy MHA</td><td>0.4671</td><td>0.1784</td></tr><tr><td>Hopfield</td><td>0.4213</td><td>0.1928</td></tr><tr><td>Full ET</td><td>0.4421</td><td>0.1785</td></tr>
</tbody></table>
<p>The modules exhibit field-dependent trade-offs. The full model does not minimize every pointwise error.</p>
</section>
</div>

<!-- Both tables report source test relative errors on different benchmarks. Do not interpret the module table as a matched spectral ablation. -->

---
chapter: '5'
appendix: A5
routeAlias: appendix-et-cost
section: Backup · Energy Transformer inference cost
source: 'Thesis Chapter 5 · tab:et:timing · Single NVIDIA A6000; 12 inference iterations'
---

# Energy Transformer: Computational Cost

<div class="appendix-content appendix-wide-left">
<section>
<h2>Reported training and inference times</h2>
<table><thead><tr><th>Benchmark</th><th>Offline training</th><th>Per snapshot</th></tr></thead><tbody>
<tr><td>Vortex street</td><td>≈ 90 min</td><td>≈ 2.7 ms</td></tr>
<tr><td>Schlieren jet</td><td>≈ 150 min</td><td>≈ 2.5 ms</td></tr>
<tr><td>3D jet</td><td>≈ 70 min</td><td>≈ 100 ms</td></tr>
</tbody></table>
<p>Measurements use a single NVIDIA A6000 and 12 inference iterations per snapshot.</p>
</section>
<section class="detail-box">
<h2>Offline training</h2><p>Learn the energy parameters once from the training distribution.</p>
<h2>Iterative inference</h2><p>Keep the learned parameters fixed. For each new snapshot, evolve the tokens through 12 energy-gradient updates, then decode the reconstructed field.</p>
<p>Training time and per-snapshot inference time measure different stages. These are source timings, not a matched runtime comparison with RFormer.</p>
</section>
</div>

<!-- The duplicated 3D-jet module ablation is retained only on A4. Times are source measurements, not presentation/export timings. -->

---
chapter: '6'
appendix: A6
routeAlias: appendix-rformer
section: Backup · RFormer baselines
source: 'Thesis Chapter 6 · tab:rformer:vortex · Total test relative RMSE, mean ± standard deviation'
---

# RFormer: Vortex-Street Baselines

<div class="appendix-content appendix-wide-left">
<section>
<table><thead><tr><th>Method</th><th>Total relative RMSE</th></tr></thead><tbody>
<tr class="highlight"><td>RFormer</td><td>0.0080 ± 0.0014</td></tr><tr><td>Voronoi CNN</td><td>0.0184 ± 0.0008</td></tr><tr><td>Gappy POD</td><td>0.0338 ± 0.0028</td></tr><tr><td>CNP</td><td>0.1620 ± 0.0056</td></tr><tr><td>ANP</td><td>0.1709 ± 0.0046</td></tr><tr><td>Interpolation</td><td>0.1843 ± 0.0004</td></tr><tr><td>TNP</td><td>0.3082 ± 0.0100</td></tr><tr><td>Kriging</td><td>0.6243 ± 0.0012</td></tr>
</tbody></table>
</section>
<section class="detail-box">
<h2>Benchmark</h2><p>Vortex-street reconstruction under the source observation protocol. Each method is evaluated against the physical reference fields.</p>
<h2>Metric</h2>

$$
\varepsilon=\frac{\sqrt{\sum\|\hat v-v\|^2}}{\sqrt{\sum\|v\|^2}}.
$$

<p>The table reports total test relative RMSE, with mean ± source standard deviation across snapshots.</p>
<p>The ranking applies to this vortex-street experiment; it is not transferred to weather or blood-flow reconstruction.</p>
</section>
</div>

<!-- Original source values and ranking retained. Do not substitute the averaged-grid target used in the blood-flow comparison. -->

---
chapter: '7'
appendix: A7
routeAlias: appendix-oc-regimes
section: Backup · OCFormer inference regimes
source: 'Thesis Chapter 7 · tab:oc:regimes · Protocol-specific timing, not a single universal latency'
---

# OCFormer: Three Deployment Regimes

<div class="appendix-content">
<table class="appendix-regimes"><thead><tr><th>Regime</th><th>What is trained?</th><th>Online work</th><th>Tested boundaries</th><th>Reported time</th></tr></thead><tbody>
<tr><td>Per-instance</td><td>Model for one boundary pair</td><td>Adam / L-BFGS optimization</td><td>One fixed pair</td><td>≈ 20 min</td></tr>
<tr><td>Transfer</td><td>Reusable backbone; adapt wrapper maps</td><td>Freeze backbone; fine-tune wrappers with L-BFGS</td><td>Structured / small perturbations</td><td>Seconds</td></tr>
<tr><td>Amortized</td><td>Fixed model across many training pairs</td><td>Forward pass; no weight updates</td><td>Held-out, in-distribution pairs</td><td>≈ 220 ms</td></tr>
</tbody></table>
<div class="appendix-two-col appendix-regime-notes">
<section><h2>Reading the main examples</h2><p>The boundary-perturbation examples use transfer with adaptation. The 3D per-instance examples do not establish amortized 3D inference.</p></section>
<section><h2>Reading the timing</h2><p>These are protocol-specific source timings, not a matched speed comparison. Transfer cost depends on perturbation size; amortized timing applies to the tested 2D distribution.</p></section>
</div>
</div>

<!-- Source timings are unchanged. Training/export Slurm job durations are unrelated to inference performance. -->

---
chapter: '7'
appendix: A8
routeAlias: appendix-oc-generalization
section: Backup · OCFormer amortized generalization
source: 'Thesis Chapter 7 · tab:oc:amortized · 100 rotated training pairs; JIT forward-pass timing over 100 runs'
---

# OCFormer: Amortized Generalization

<div class="appendix-content">
<p>Held-out rotations of 2D antipodal configurations; 100 rotated training pairs. JIT forward-pass timing is measured over 100 runs.</p>
<table><thead><tr><th>M</th><th>Test cost</th><th>Lower bound gap</th><th>Sampled feasible cases</th><th>Inference</th></tr></thead><tbody>
<tr><td>8</td><td>0.4053</td><td>1.3%</td><td>100%</td><td>218.6 ± 1.3 ms</td></tr><tr><td>16</td><td>0.8399</td><td>5.0%</td><td>75%</td><td>220.9 ± 1.2 ms</td></tr>
</tbody></table>
<div class="appendix-two-col appendix-metric-definitions">
<section class="detail-box"><h2>Cost relative to free motion</h2>

$$
J_{\mathrm{LB}}=\sum_i\frac{\|x_i^T-x_i^0\|^2}{2T},\qquad
\mathrm{gap}=\frac{J-J_{\mathrm{LB}}}{J_{\mathrm{LB}}}.
$$

<p>The lower bound omits collision constraints. The gap is not measured against the unknown constrained optimum.</p>
</section>
<section class="detail-box"><h2>Sampled feasibility</h2>

$$
c_{\min}=\min_{i<j,t_k}\bigl(\|x_i(t_k)-x_j(t_k)\|-2r\bigr).
$$

<p>A case passes when its minimum sampled clearance is positive. At <InlineMath tex="M=16" />, 25% of held-out cases fail this test; sampled clearance does not certify continuous-time feasibility.</p>
</section>
</div>
</div>

<!-- Source means, gaps, feasible fractions, and timing uncertainty retained. Demonstrated coverage is zero-shot rotated pairs, not arbitrary boundaries, variable M, or amortized 3D. Full cost uncertainty is retained in the thesis table. -->
