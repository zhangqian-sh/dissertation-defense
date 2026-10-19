---
chapter: '5'
section: Part II · Sequence-to-sequence modeling
source: 'Thesis Chapter 5 · Chapter overview'
divider: part
---

<p class="divider-chapter">Chapter 5</p>
<div class="divider-rule" aria-hidden="true"></div>

# Reconstruction from Sparse Measurements:<br>An Energy Transformer Approach

<!-- Spoken transition: How to reconstruct flow fields with vision-based model?

Begin the independent second theme: field reconstruction and trajectory inference. This Energy Transformer study does not receive outputs from the preceding spiking methods. -->

---
chapter: '5'
section: Energy Transformer · Reconstruction
source: 'Thesis Chapter 5 · fig:et:workflow · Reconstruction from Sparse
  Measurements:<br>An Energy Transformer Approach'
---

# Reconstruction Operator Learning

<div class="et-reconstruction-layout">
<section class="et-reconstruction-description">
<h2>Reconstruction operator</h2>
<p>A map from the <strong>space of sparsely observed functions</strong> to the <strong>space of fully reconstructed functions</strong>.</p>

$$
\mathcal R:\;v|_{\Omega_{\mathcal O}}\longmapsto\widehat v,
\qquad \widehat v:\Omega\to\mathbb R^{d_v}
$$

<p>Observed position–value pairs represent the input function. Evaluate the reconstructed function at an unobserved position:</p>

$$
\widehat v_a^{A'_j}=\mathcal R\!\left(x_a^{A'_j};\widetilde{\mathcal P}_a\right),
\quad A'_j\notin\mathcal O_a
$$

<h2 class="et-reconstruction-subheading">Energy Transformer realizes this map</h2>
<p>ET realizes the operator on a <strong>regular patch lattice</strong>, mapping observed patches to a completed field.</p>
<ul>
<li><strong>Representation:</strong> tokenize observations; initialize missing tokens with noise.</li>
<li><strong>Learning:</strong> learn energy by denoising the masked snapshots.</li>
<li><strong>Reconstruction:</strong> update tokens by minimizing the learned energy, then decode and depatch.</li>
</ul>
</section>
<figure class="figure et-reconstruction-workflow">
<h2>Reconstruction workflow</h2>
<img src="/figures/ch05/et-workflow.png" alt="Energy Transformer reconstruction: observed field to patches, tokenizer, energy-based token completion, detokenizer and reconstructed field; dashed paths are training-only">
<figcaption>Patch → tokenize → complete → decode → depatch</figcaption>
<p class="et-reconstruction-note">Dashed arrows: training-only operations. All tokens evolve during inference.</p>
</figure>
</div>

<!--
This begins the independent reconstruction part. There is no demonstrated SNN-to-reconstruction-to-control pipeline.
-->

---
chapter: '5'
section: Energy Transformer · Token dynamics
source: 'Thesis Chapter 5 · fig:et:architecture; eq:et:update · Niter=12, step
  size 0.1; tab:et:hyperparameters'
---

# Energy Transformer

<div class="et-method-layout">
<div class="et-method-explanation">
<section>
<h2>What is Energy Transformer?</h2>
<p>An associative energy model for patch tokens. Its learned energy combines relationships across tokens with memory within each token.</p>

$$
E_\theta(g)=E_\theta^{\mathrm{MHA}}(g)+E_\theta^{\mathrm{HN}}(g)
$$

</section>
<section>
<h2>Inference · evolve the state tokens</h2>
<p>Initialize tokens from observations and noise. Keep the learned energy fixed and update the token state:</p>

$$
\begin{aligned}
g^{(t)}&=\mathrm{LN}_\theta(x^{(t)}),\\
x^{(t+1)}&=x^{(t)}-\alpha\nabla_g E_\theta(g^{(t)}).
\end{aligned}
$$

</section>
<section>
<h2>Learning · fit the energy surface</h2>
<div class="et-learning-illustration">
<div>
<p>Fit the decoded endpoint to the complete field. Decoder D maps tokens back to the field.</p>

$$
\begin{aligned}
\widehat w_\theta&=D_\theta\!\left(x^{(T)}\right),\\
\min_\theta\;&\mathbb E_{w,m}\!\left[\ell(\widehat w_\theta,w)\right].
\end{aligned}
$$

<p>Differentiate through the token updates to shape the energy surface.</p>
</div>
<EnergyLearningBowl />
</div>
</section>
</div>
<div class="et-method-energy et-flow-explanation">
<section class="et-energy-annotation">
<h2>MHA · interactions across tokens</h2>
<p>Query–key affinities couple compatible patterns across patches.</p>

$$
E_\theta^{\mathrm{MHA}}=-\frac1\beta\sum_{h=1}^{H}\sum_{C=1}^{N}
\log\!\left(\sum_{B\ne C}e^{\beta A_{hBC}}\right)
$$

$$
A_{hBC}=(W_h^K g_B)^\mathsf T(W_h^Q g_C)
$$

</section>
<EnergyTransformerFlow />
<section class="et-energy-annotation">
<h2>HN · memory within each token</h2>
<p>Learned memory vectors favor familiar local patch patterns.</p>

$$
E_\theta^{\mathrm{HN}}=-\sum_{B=1}^{N}\sum_{\mu=1}^{K}
G\!\left(\xi_\mu^\mathsf T g_B\right)
$$

</section>
</div>
</div>

<!--
Source: ET manuscript, energy-attention / Hopfield formulas and normalized-coordinate dynamics. Training regresses the finite-unroll decoded state; no claim of exact minimization, clamped observations or guaranteed monotone energy descent.
-->

---
chapter: '5'
section: Energy Transformer · Reconstruction history
source: 'ETRO 2D vortex street · test sample 0 · 90% nominal masking · α=0.1 ·
  Replay/archived output ΔL₂=0.111%'
---

# Example: 2d Vortex Street

<EnergyHistory />

<!--
Demo: compare saved masked input and reference, then play updates 1–12 or scroll over the fields. This is the 2D vortex-street v component at native 128×256 resolution, shown without display smoothing. Energy covers all tokens; error covers v. Replay differs from archived output by 0.111% relative L2, with unresolved cause; history endpoint agrees with ordinary inference in the replay runtime.
-->

---
chapter: '5'
section: Energy Transformer · Field reconstruction
source: 'Thesis Chapter 5 · fig:et:3djet-results · Native published
  cross-sections; tab:et:3djet-errors'
---

# Example: 3D Turbulent Jet Flow

<div class="et-jet-layout">
<section class="et-jet-setup">
<JetReconstructionSetup />
</section>
<section class="et-jet-panels" aria-label="Reference, sparse observations and ET reconstruction for u, v and p">
<JetTestLoop />
<p class="et-jet-metrics">Relative L2 error: velocity <InlineMath tex="\mathbf{u}=(u,v,w)" /> 0.4421; pressure <InlineMath tex="p" /> 0.1785.</p>
</section>
</div>

<!--
Apparatus is a simplified schematic based on Cai, Gray and Karniadakis (2024), DOI 10.1109/TIM.2024.3398068, Section III and Fig. 2 caption. The precise apparatus geometry was not available from the blocked IEEE figure; camera placement is illustrative. Source text verified using the author-uploaded manuscript: https://www.researchgate.net/publication/380446513_Physics-Informed_Neural_Networks_Enhanced_Particle_Tracking_Velocimetry_An_Example_for_Turbulent_Jet_Flow. Published ET result panels retain the native source slice and orientation.
-->

---
chapter: '5'
section: Energy Transformer · Pointwise and spectral fidelity
source: 'Thesis Chapter 5 · fig:et:pinn-rel-err; fig:et:pinn-spectrum;
  sec:et:fidelity · Turbulent-jet benchmark'
---

# Example: 3d Turbulent Flow

<div class="et-fidelity-layout">
<section class="et-fidelity-explanation">
<h2>Pointwise error</h2>
<p>Relative L2 measures the overall discrepancy between reconstructed and reference fields. It does not distinguish errors at different spatial scales.</p>
<h2>Kinetic-energy spectrum</h2>
<p>The spectrum measures how kinetic energy is distributed across spatial scales. Larger wavenumbers correspond to finer structures.</p>
<div class="et-fidelity-conclusion">
<p>Energy Transforme has higher velocity relative L2 error than PINN, but better preserves the energy spectrum. Lower pointwise error itself does not imply better reconstruction of turbulent flow at fine scales.</p>
</div>
</section>
<section class="et-fidelity-plots" aria-label="Pointwise errors above and kinetic-energy spectra below; PINN left and Energy Transformer right">
<figure class="figure"><img src="/figures/ch05/et-pinn-rel-err.png" alt="PINN velocity and pressure relative errors"/><figcaption>PINN</figcaption></figure>
<figure class="figure"><img src="/figures/ch05/et-rel-err.png" alt="Energy Transformer velocity and pressure relative errors"/><figcaption>Energy Transformer</figcaption></figure>
<figure class="figure"><img src="/figures/ch05/et-pinn-spectrum.png" alt="PINN kinetic-energy spectrum with attenuated high-wavenumber energy"/><figcaption>PINN</figcaption></figure>
<figure class="figure"><img src="/figures/ch05/et-spectrum.png" alt="Energy Transformer kinetic-energy spectrum with improved high-wavenumber retention"/><figcaption>Energy Transformer</figcaption></figure>
</section>
</div>

<!--
Plots retain source normalization. Spectral fidelity does not imply uniformly lower pointwise error.
-->
