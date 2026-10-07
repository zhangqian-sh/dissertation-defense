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

For parameters $\theta\in\mathbb R^d$, choose a random direction $v$. Like a directional finite difference, the JVP measures how the loss changes along $v$:

$$
\frac{\mathcal L(\theta+\epsilon v)-\mathcal L(\theta)}{\epsilon}
\approx d_v=\nabla_\theta\mathcal L^\top v.
$$

Forward-mode differentiation computes $d_v$ directly; it does not use a finite-difference step $\epsilon$. For hard spikes, evaluate the JVP with the surrogate derivative $f_{SG}'(a)=\frac{e^{-a^2/(2\sigma^2)}}{\sigma\sqrt{2\pi}}$, where $a=U-U_{th}$.

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
source: 'Thesis Chapter 4 · fig:rfg:box-large; fig:rfg:darcy · Darcy without
  skip connections; WSG jobs 7076193 and 7076196'
---

# Weak Surrogate Gradients

<div class="wsg-performance">
<section class="wsg-method">
<h2>WSG: estimate derivatives from spike responses</h2>

Replace direct evaluation of a smooth surrogate with sampled responses of the hard spike map $H$. For the distance to threshold $a=U-U_{th}$:

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

$-\nabla\!\cdot(a\nabla u)=f,\qquad a\mapsto u$

<DarcyErrorBars />
<p class="wsg-note">SG / WSG: mean ± SD over test samples.</p>
</section>
</section>
<section class="wsg-darcy-results">
<h2>Example: 2D Darcy equation</h2>

<div class="wsg-poisson-setup">

$-\nabla\!\cdot(a\nabla u)=f,\qquad\mathcal G_\theta:a\mapsto u$

</div>
<div class="wsg-darcy-panels">
<figure class="figure"><img src="/figures/ch04/darcy_bp.png" alt="Historical Darcy prediction using backpropagation"><figcaption>BP</figcaption></figure>
<figure class="figure"><img src="/figures/ch04/darcy_global.png" alt="Historical Darcy prediction using global SG"><figcaption>SG · Global</figcaption></figure>
<figure class="figure"><img src="/figures/ch04/darcy_local.png" alt="Historical Darcy prediction using layerwise SG"><figcaption>SG · Layerwise</figcaption></figure>
<figure class="figure"><img src="/figures/ch04/darcy_wsg_global_styled.png" alt="Global WSG prediction from the training-selected checkpoint"><figcaption>WSG · Global</figcaption></figure>
<figure class="figure"><img src="/figures/ch04/darcy_wsg_layerwise_styled.png" alt="Layerwise WSG prediction from the training-selected checkpoint"><figcaption>WSG · Layerwise</figcaption></figure>
</div>
<p class="wsg-note">WSG: 400k updates; $\sigma=0.5$, $K=500$; training-selected checkpoints.<br>Global: 8 directions/update; layerwise: 1/layer. SG panels are historical.</p>
</section>
</div>

<!--
SG values and the BP panel are historical no-skip results from fig:rfg:box-large and fig:rfg:darcy; they are not matched reruns.
WSG results: jobs 7076193 (global) and 7076196 (layerwise), 400000 full-batch updates, seed 42, sigma .5, 500 WSG threshold samples, Adam 1e-4, 1000 train / 200 test samples, 32 spike steps, no skip connections.
Checkpoint selection uses lowest logged training error: global epoch 393000, test .0842583 ± .0357181; layerwise epoch 391000, test .0751678 ± .0344492.
Final-update errors: global .0875326 ± .0352131; layerwise .0795784 ± .0329169. The bar chart uses training-selected checkpoints, matching the WSG prediction panels.
Global averages 8 full-network directions; layerwise uses 1 direction for each of 11 layers. Probe budgets differ; these single-seed results do not isolate estimation method alone.
Analysis: data/raw/ch04/darcy_wsg/analysis-7076193-7076196/analysis.md.
-->
