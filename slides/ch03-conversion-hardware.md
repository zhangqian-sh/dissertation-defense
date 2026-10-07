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

# Calibrate the local mismatch before it propagates

<div class="density">
<div class="density-grid ">
<div class="detail-box"><h2>Layerwise calibration · l = 1,…,L</h2><ol class="algorithm"><li>Train the smooth ANN; select calibration inputs.</li><li>Freeze layers 1,…,l−1; feed their decoded spikes forward.</li><li>Compare ANN activation f with the IF output average.</li><li>Update current weights/biases with Adam; freeze and advance.</li></ol>
<div class="math-panel">

$$
\begin{aligned}\min_{W_l,b_l}&\ \|e_{c,l}\|_2^2\\e_{c,l}&=f(z_l)-\overline{\mathrm{IF}}_T(z_l)\end{aligned}
$$

</div>
</div>
<div class="detail-box"><h2>Local mismatch → final output error</h2>
<div class="math-panel">

$$
\begin{aligned}e_L^\top H_L e_L&\le\sum_{l=1}^{L}2^{L-l+1}e_{c,l}^\top B_l e_{c,l}\\B_l&=H_l+C_l\sqrt{\mathcal L_{ANN}}I\end{aligned}
$$

</div>
<p class="small">H: loss Hessian; C: derivative/curvature bound. Early-layer mismatch is amplified; ANN training loss affects the bound.</p><figure class="figure"><img style="height:150px" src="/figures/ch03/calibration_data_size.png" alt="Separate sin(x) study · calibration-data size"><figcaption>Separate sin(x) study · calibration-data size</figcaption></figure></div>
</div><p class="protocol">Bound assumes approximable activation values/first derivatives and bounded second derivatives · floating-point analysis</p>
</div>

<!-- The thesis extends the ReLU-specific argument to activations with approximable values/first derivatives and bounded second derivatives. Define the compact bound and its assumptions; it is an upper bound, not an exact prediction of measured error. -->

---
chapter: '3'
section: ANN-to-SNN conversion · Field fidelity
source: 'Thesis Chapter 3 · fig:conversion:poisson · Published matched Poisson comparison; tab:conversion:accuracy'
---

# Calibration restores the spatial solution

<div class="density">
<div class="four"><figure class="figure"><img style="height:235px" src="/figures/ch03/poisson_true.png" alt="Numerical reference"><figcaption>Numerical reference</figcaption></figure><figure class="figure"><img style="height:235px" src="/figures/ch03/poisson_ann.png" alt="ANN / PINN"><figcaption>ANN / PINN</figcaption></figure><figure class="figure"><img style="height:235px" src="/figures/ch03/poisson_snn_none.png" alt="SNN · weight copying"><figcaption>SNN · weight copying</figcaption></figure><figure class="figure"><img style="height:235px" src="/figures/ch03/poisson_snn_calibrated.png" alt="SNN · calibrated"><figcaption>SNN · calibrated</figcaption></figure></div><div class="density-grid ">
<div class="detail-box"><h2>Matched Poisson experiment</h2><p class="small">Thesis domain [−1,1]²; source panels retain [0,1] plotting axes. Homogeneous Dirichlet boundaries · tanh PINN, 3 hidden layers × 100.</p>
<div class="math-panel">

$$
-\Delta u=f,\qquad u|_{\partial\Omega}=0
$$

</div>
</div>
<div class="detail-box"><h2>Reported conversion fidelity</h2><p class="small"><strong>SNN-to-ANN relative L₂:</strong> 0.0471<br><strong>Spike rate:</strong> 0.373</p><p class="small">Calibration recovers the spatial pattern. This conversion metric uses the trained ANN field as its target.</p></div>
</div>
</div>

<!-- Retain the original panels and color scales. ANN-to-reference error and SNN-to-ANN conversion error are different quantities. -->

---
chapter: '3'
section: ANN-to-SNN conversion · Simulation horizon
source: 'Thesis Chapter 3 · fig:conversion:sin-horizon · Separately configured simulation horizons; fig:conversion:error-horizon'
---

# More spike steps refine the approximation

<div class="density">
<div class="three"><figure class="figure"><img style="height:190px" src="/figures/ch03/sin_diff_T8.png" alt="Separately configured T = 8"><figcaption>Separately configured T = 8</figcaption></figure><figure class="figure"><img style="height:190px" src="/figures/ch03/sin_diff_T32.png" alt="Separately configured T = 32"><figcaption>Separately configured T = 32</figcaption></figure><figure class="figure"><img style="height:190px" src="/figures/ch03/sin_diff_T128.png" alt="Separately configured T = 128"><figcaption>Separately configured T = 128</figcaption></figure></div><div class="density-grid ">
<figure class="figure"><img style="height:160px" src="/figures/ch03/error_vs_T_L2.png" alt="Separate depth-2 sweep · source widths and error axis"><figcaption>Separate depth-2 sweep · source widths and error axis</figcaption></figure>
<div class="detail-box"><h2>Resolution and an accuracy floor</h2><p class="small">Finite-step spike averages become finer as T increases. The source sin(x) study shows roughly 1/T decay for moderate T, then saturation.</p><p class="small">Residual activation mismatch and ANN error remain. This horizon sweep differs from prefixes of one fixed calibrated SNN.</p></div>
</div>
</div>

<!-- These are the published separately configured T examples. The next slide instead inspects cumulative prefixes of one fixed T=128 conversion. -->

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

<div class="density">
<div class="density-grid ">
<figure class="figure"><img style="height:320px" src="/figures/ch03/loihi_precision_results.png" alt="Source Poisson comparison · CPU / two hardware precisions"><figcaption>Source Poisson comparison · CPU / two hardware precisions</figcaption></figure>
<div class="detail-box"><h2>Quantization and connection budget</h2><table><thead><tr><th>Platform / precision</th><th>RMS</th></tr></thead><tbody><tr><td>CPU</td><td>0.0131</td></tr><tr><td>Loihi · 8-bit</td><td>0.0215</td></tr><tr><td>Loihi · effective 16-bit</td><td>0.0160</td></tr></tbody></table><div class="connection-map"><span>8-bit connection A</span><span>8-bit connection B</span><b>↘ &nbsp; combined weight contribution &nbsp; ↙</b></div><p class="small">Two 8-bit connections represent each effective 16-bit weight; improved fidelity uses more connections.</p></div>
</div><p class="protocol">Source-reported RMS · physical units/normalization not independently recovered · distinct from floating-point conversion error</p>
</div>

<!-- Keep the source metric terminology. Do not compare these numbers with the relative L2 values from other chapters. -->

---
chapter: '3'
section: Loihi 2 · Measured scaling
source: 'Thesis Chapter 3 · fig:loihi:throughput; fig:loihi:epi; fig:loihi:edp · Measurement scope excludes I/O'
---

# Replication changes throughput and energy cost

<div class="density">
<div class="three"><figure class="figure"><img style="height:265px" src="/figures/ch03/loihi_throughput.png" alt="Throughput · both precisions"><figcaption>Throughput · both precisions</figcaption></figure><figure class="figure"><img style="height:265px" src="/figures/ch03/loihi_epi.png" alt="Energy per inference"><figcaption>Energy per inference</figcaption></figure><figure class="figure"><img style="height:265px" src="/figures/ch03/loihi_edp.png" alt="Energy–delay product"><figcaption>Energy–delay product</figcaption></figure></div>
<div class="math-panel">

$$
\mathrm{throughput}=\frac{N_{\mathrm{inferences}}}{\Delta t},\quad \mathrm{EPI}=\frac{E_{\mathrm{measured}}}{N_{\mathrm{inferences}}},\quad \mathrm{EDP}=\mathrm{EPI}\times\mathrm{delay}
$$

</div>
<p class="protocol">Parallel replicas share the workload · transition near 70 replicas involves multiple chips · energy excludes I/O · no CPU energy multiplier</p>
</div>

<!-- These are measured source curves, not extrapolated CPU-versus-Loihi energy claims. No CPU energy multiplier is available. -->
