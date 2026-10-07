---
chapter: '5'
section: Part II · Sequence-to-sequence modeling
source: 'Thesis Chapter 5 · Chapter overview'
divider: part
---

<p class="divider-chapter">Chapter 5</p>
<div class="divider-rule" aria-hidden="true"></div>

# Reconstruction from Sparse Measurements: An Energy Transformer Approach

<!-- Spoken transition: How to reconstruct flow fields with vision-based model?

Begin the independent second theme: field reconstruction and trajectory inference. This Energy Transformer study does not receive outputs from the preceding spiking methods. -->

---
chapter: '5'
section: Energy Transformer · Reconstruction
source: 'Thesis Chapter 5 · fig:et:workflow · Reconstruction from sparse observations; tab:et:hyperparameters'
---

# Infer a complete field from partial observations

<div class="density">
<div class="density-grid ">
<div class="detail-box"><h2>Structured patches → field completion</h2>
<div class="math-panel">

$$
w_B\in\mathbb R^{p_1\cdots p_d d_v}\;\longrightarrow\;x_B\in\mathbb R^{256}
$$

</div>
<p class="small"><strong>Observed patches:</strong> tokenize measured channels.</p><p class="small"><strong>Masked patches:</strong> initialize tokens with random noise.</p><p class="small"><strong>Training:</strong> complete snapshots generate masked input/target pairs.</p><p class="small"><strong>Inference:</strong> hold weights fixed; refine tokens, detokenize, and depatch.</p></div>
<figure class="figure"><img style="height:320px" src="/figures/ch05/et-workflow.png" alt="Source workflow · patch / tokenize / complete / decode"><figcaption>Source workflow · patch / tokenize / complete / decode</figcaption></figure>
</div><p class="protocol">Patch size 8×8 (2D), 8×8×8 (3D) · token width 256 · tokenizer/detokenizer hidden width 256 · structured lattice</p>
</div>

<!-- This begins the independent reconstruction part. There is no demonstrated SNN-to-reconstruction-to-control pipeline. -->

---
chapter: '5'
section: Energy Transformer · Token dynamics
source: 'Thesis Chapter 5 · fig:et:architecture; eq:et:update · Niter=12, step size 0.1; tab:et:hyperparameters'
---

# At inference, tokens move through a learned energy

<div class="density">
<div class="density-grid ">
<figure class="figure"><img style="height:235px" src="/figures/ch05/et-block.png" alt="Energy attention: inter-token coupling · Hopfield: within-token memory"><figcaption>Energy attention: inter-token coupling · Hopfield: within-token memory</figcaption></figure>
<div class="detail-box"><h2>Learned energy; evolving token state</h2>
<div class="math-panel">

$$
E=E^{ATT}+E^{HN},\qquad g=\mathrm{LN}(x)
$$

</div>

<div class="math-panel">

$$
x^{(n+1)}=x^{(n)}-\alpha\nabla_g E(g(x^{(n)}))
$$

</div>
<p class="small">Differentiate energy with respect to normalized coordinates g; n is an inference iteration.</p></div>
</div><div class="step-chain"><span>Initialize x⁽⁰⁾</span><b>→</b><span>Normalize g</span><b>→</b><span>Evaluate E, update x</span><b>↻ 12</b><span>Decode field</span></div><p class="protocol">α = 0.1 · 8 attention heads · 2048 Hopfield units · weights fixed; all tokens participate · no monotonic-descent guarantee</p>
</div>

<!-- This diagram explains the update. The following slide replays the saved masked input through the saved checkpoint. Do not imply monotonic energy decrease or clamped observed tokens. -->

---
chapter: '5'
section: Energy Transformer · Reconstruction history
source: 'ETRO 2D vortex street · test sample 0 · 90% nominal masking · α=0.1 · Replay/archived output ΔL₂=0.111%'
---

# Follow reconstruction through the token updates

<EnergyHistory />

<!-- Demo: compare saved masked input and reference, then play updates 1–12 or scroll over the fields. This is the 2D vortex-street v component at native 128×256 resolution, shown without display smoothing. Energy covers all tokens; error covers v. Replay differs from archived output by 0.111% relative L2, with unresolved cause; history endpoint agrees with ordinary inference in the replay runtime. -->

---
chapter: '5'
section: Energy Transformer · Field reconstruction
source: 'Thesis Chapter 5 · fig:et:3djet-results · Native published cross-sections; tab:et:3djet-errors'
---

# Reconstruct spatial structure in a turbulent jet

<div class="density">
<div class="density-grid jet-results">
<div class="density">
<figure class="figure"><img style="height:165px" src="/figures/ch05/et-3djet-results-u.png" alt="Streamwise velocity: source reference, sparse observations and ET"><figcaption>u · streamwise velocity · reference / observations / ET</figcaption></figure>
<figure class="figure"><img style="height:165px" src="/figures/ch05/et-3djet-results-v.png" alt="Cross-stream velocity: source reference, sparse observations and ET"><figcaption>v · cross-stream velocity · reference / observations / ET</figcaption></figure>
</div>
<div class="detail-box"><h2>Pressure and aggregate fidelity</h2>
<figure class="figure"><img style="height:150px" src="/figures/ch05/et-3djet-results-p.png" alt="Pressure: source reference, sparse observations and ET"><figcaption>p · pressure · same source cross-section</figcaption></figure>
<table><thead><tr><th>Field</th><th>Relative error</th></tr></thead><tbody><tr><td>Velocity (u,v,w)</td><td>0.4421</td></tr><tr><td>Pressure p</td><td>0.1785</td></tr></tbody></table>
<p class="small">Coherent structure is recovered; velocity fidelity remains harder than pressure on this benchmark.</p>
</div>
</div>
<p class="protocol">Published z = 0 slice · test index 180 · 80% patch masking · aggregate metrics describe the source test set, not only this slice.</p>
</div>

<!-- These are fixed source slices, not a reconstruction of arbitrary 3D values from images. Discuss the correspondence of coherent structures before turning to quantitative fidelity. -->

---
chapter: '5'
section: Energy Transformer · Pointwise fidelity
source: 'Thesis Chapter 5 · fig:et:pinn-rel-err; sec:et:fidelity · Source 3D turbulent-jet test interval'
---

# Pointwise error is one part of physical fidelity

<div class="density">
<div class="density-grid ">
<figure class="figure"><img style="height:280px" src="/figures/ch05/et-pinn-rel-err.png" alt="PINN · velocity and pressure errors"><figcaption>PINN · velocity and pressure errors</figcaption></figure>
<figure class="figure"><img style="height:280px" src="/figures/ch05/et-rel-err.png" alt="ET · same source turbulent-jet benchmark"><figcaption>ET · same source turbulent-jet benchmark</figcaption></figure>
</div>
<div class="math-panel">

$$
\varepsilon=\frac{\|\hat q-q\|_2}{\|q\|_2},\qquad q=\text{velocity or pressure}
$$

</div>
<p class="protocol">Source test interval · PINN can have lower pointwise velocity error · these curves alone do not assess missing fine-scale energy</p>
</div>

<!-- Keep this limitation explicit. The next slide supplies kinetic-energy spectra, not a claim that ET dominates all metrics. -->

---
chapter: '5'
section: Energy Transformer · Spectral fidelity
source: 'Thesis Chapter 5 · fig:et:pinn-spectrum · Kinetic-energy spectra on the turbulent-jet benchmark'
---

# Spectra reveal fine scales that errors can miss

<div class="density">
<div class="density-grid ">
<figure class="figure"><img style="height:280px" src="/figures/ch05/et-pinn-spectrum.png" alt="PINN · high-wavenumber energy attenuated"><figcaption>PINN · high-wavenumber energy attenuated</figcaption></figure>
<figure class="figure"><img style="height:280px" src="/figures/ch05/et-spectrum.png" alt="ET · improved high-wavenumber retention"><figcaption>ET · improved high-wavenumber retention</figcaption></figure>
</div>
<div class="math-panel">

$$
E(k)=\frac12\sum_{\boldsymbol\kappa\,\in\,\mathrm{shell}(k)}\left|\widehat{\mathbf u}(\boldsymbol\kappa)\right|^2
$$

</div>
<p class="protocol">Kinetic-energy spectrum · k identifies spatial scale · formula shows shell-energy interpretation; retain source normalization · evaluate alongside pointwise errors</p>
</div>

<!-- Pair the conclusion with the preceding error plots. Do not translate spectral fidelity into uniformly lower pointwise error. -->

---
chapter: '5'
section: Energy Transformer · Inference cost
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
