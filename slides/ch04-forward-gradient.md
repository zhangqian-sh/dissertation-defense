---
chapter: '4'
section: Part I · Neuromorphic algorithms
source: 'Thesis Chapter 4 · Chapter overview'
divider: chapter
---

<p class="divider-chapter">Chapter 4</p>
<div class="divider-rule" aria-hidden="true"></div>

# Direct SNN Training with Randomized Forward-Mode Gradients

<!-- Spoken transition: Training: How to train SciML model with spiking mechanism?

Move from conversion and deployment to training. Explain directional derivatives and their accuracy trade-offs without claiming measured training-energy savings. -->

---
chapter: '4'
section: Randomized forward gradients · Method
source: 'Thesis Chapter 4 · sec:rfg:estimator; eq:rfg:directional; eq:rfg:global; eq:rfg:layerwise; eq:rfg:sg'
---

# Forward Mode Gradient

<div class="density">

<div class="rfg-jvp-intro">
<section>
<h2>JVP: probe the loss along a direction</h2>

For parameters $\theta\in\mathbb R^d$ and a direction $v$, the JVP computes the directional derivative of the loss:

$$
d_v=\operatorname{JVP}(\mathcal L,\theta;v)
=\nabla_\theta\mathcal L^\top v.
$$

Forward-mode automatic differentiation propagates directional derivatives through the network. For hard spikes, use the surrogate derivative $f_{SG}'(a)=\frac{e^{-a^2/(2\sigma^2)}}{\sigma\sqrt{2\pi}}$, where $a=U-U_{th}$.

</section>
<section>
<h2>Random probes → estimated gradient → GD</h2>

In a high-dimensional parameter space, sample $v\sim\mathbf P$ and use its directional slope to form a stochastic gradient estimate:

$$
\hat g=d_vv,\qquad\theta\leftarrow\theta-\eta\hat g.
$$

Resample directions during training. Update with $\hat g$ instead of explicitly computing every component of the full gradient.

</section>
</div>
<RFGDirections />
<p class="rfg-diagram-note">Shared layers have identical weights but carry distinct activations. Directional slopes use JVP; source directions: Bernoulli($p=\tfrac12$).</p>

</div>

<!-- Source experiments describe Bernoulli parameter perturbations. Gaussian threshold shifts belong to the weak surrogate, not the same sampling operation. No measured training-energy savings are claimed. -->

---
chapter: '4'
section: Randomized forward gradients · Weak surrogate
source: 'Matched Darcy runs · SG: 7093209, 7092847, 7092859 · WSG: 7098047, 7076193, 7076196'
---

# Weak Surrogate Gradients

<div class="wsg-performance">
<section class="wsg-method">
<h2>WSG: stochastic finite-difference analogy</h2>

Randomly perturb the hard spike map $H$ and average weighted output differences to estimate its Gaussian-smoothed derivative. Let $a=U-U_{th}$ denote distance to threshold:

<ol class="wsg-computation">
<li>

Sample Gaussian shifts $\delta_j\sim\mathcal N(0,\sigma^2)$.

</li>
<li>

Measure the spike change $H(a+\delta_j)-H(a)$.

</li>
<li>

Average the weighted responses:

</li>
</ol>

$$
f_{\mathrm{WSG}}'(a)=\frac1K\sum_{j=1}^K\frac{\delta_j}{\sigma^2}\left[H(a+\delta_j)-H(a)\right].
$$

Use the estimate in BP or JVP; the forward pass retains hard spikes.

<section class="wsg-darcy">
<h2>Darcy · training methods</h2>

<DarcyErrorBars />
</section>
</section>
<section class="wsg-darcy-results">
<h2>Example: 2D Darcy equation</h2>

<div class="wsg-poisson-setup">

$-\nabla\!\cdot(a\nabla u)=f,\qquad\mathcal G_\theta:a\mapsto u$

</div>
<div class="wsg-darcy-panels">
<figure class="figure"><img src="/figures/ch04/darcy_sg_bp.png" alt="Matched SG-BP prediction for test sample 0"><figcaption>SG · BP</figcaption></figure>
<figure class="figure"><img src="/figures/ch04/darcy_sg_global.png" alt="Matched global SG prediction for test sample 0"><figcaption>SG · Global</figcaption></figure>
<figure class="figure"><img src="/figures/ch04/darcy_sg_layerwise.png" alt="Matched layerwise SG prediction for test sample 0"><figcaption>SG · Layerwise</figcaption></figure>
<figure class="figure"><img src="/figures/ch04/darcy_wsg_bp.png" alt="Optimized WSG-BP prediction for test sample 0"><figcaption>WSG · BP</figcaption></figure>
<figure class="figure"><img src="/figures/ch04/darcy_wsg_global.png" alt="Matched global WSG prediction for test sample 0"><figcaption>WSG · Global</figcaption></figure>
<figure class="figure"><img src="/figures/ch04/darcy_wsg_layerwise.png" alt="Matched layerwise WSG prediction for test sample 0"><figcaption>WSG · Layerwise</figcaption></figure>
</div>
</section>
</div>

<!--
All six panels and bars now use matched reruns: SG BP 7093209, global 7092847, layerwise 7092859; WSG optimized BP 7098047, global 7076193, layerwise 7076196.
400000 full-batch updates, seed 42, sigma .5, 500 WSG threshold samples, Adam 1e-4, 1000 train / 200 test samples, 32 spike steps, no skip connections, 99904 parameters.
Checkpoints selected by lowest logged training error. Test relative L2 mean ± population SD:
SG-BP .0204897951 ± .0063863997 (epoch 386000); SG-global .0782655701 ± .0311860982 (387000); SG-layerwise .0744939074 ± .0315359570 (393000).
WSG-BP .0211343057 ± .0064200633 (369000); WSG-global .0842582956 ± .0357180797 (393000); WSG-layerwise .0751678199 ± .0344492272 (391000).
Panels are the saved collector prediction.png files, each displaying test sample 0 with the same reference-derived color limits. All 200 saved test references were verified identical across runs.
Global averages 8 full-network directions; layerwise uses 1 direction for each of 11 layers. These single-seed runs have different probe budgets; they do not isolate estimation method alone.
WSG-BP runtime is from the optimized scan_unrolled run; global/layerwise WSG runtimes use their original implementations.
-->
