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

# Train with directional derivatives in forward mode

<div class="density">

<div class="math-panel">

$$
d_v=\mathrm{JVP}_\theta(\mathcal L;v),\quad \hat g=d_vv,\quad \theta\leftarrow\theta-\eta\hat g
$$

</div>
<div class="step-chain"><span>1 · sample v</span><b>→</b><span>2 · forward spikes + JVP</span><b>→</b><span>3 · form ĝ and update</span></div><div class="density-grid ">
<div class="detail-box"><h2>Global direction</h2>
<div class="math-panel">

$$
v=(v^1,\ldots,v^L),\qquad \hat g^l=d_vv^l
$$

</div>
<p class="small">One direction spans all parameters; the global directional derivative supplies each layer update.</p></div>
<div class="detail-box"><h2>Layerwise directions</h2>
<div class="math-panel">

$$
\hat g^l=\mathrm{JVP}_{\theta^l}(\mathcal L;v^l)\,v^l
$$

</div>
<p class="small">Perturb one layer at a time; each layer has its own directional derivative.</p></div>
</div><p class="protocol">Source parameter directions: Bernoulli(p=½) · hard spikes forward; surrogate derivative for JVP · no measured training-energy saving</p><div class="small">

Standard surrogate near threshold: $f_{SG}^{\prime}(a)=e^{-a^2/(2\sigma^2)}/(\sigma\sqrt{2\pi})$, with $a=U-U_{th}$.

</div>
</div>

<!-- Source experiments describe Bernoulli parameter perturbations. Gaussian threshold shifts belong to the weak surrogate, not the same sampling operation. No measured training-energy savings are claimed. -->

---
chapter: '4'
section: Randomized forward gradients · Matched predictions
source: 'Thesis Chapter 4 · fig:rfg:poisson · Standard surrogate-gradient configurations; tab:rfg:poisson'
---

# Matched Poisson predictions across training methods

<div class="density">
<div class="three"><figure class="figure"><img style="height:280px" src="/figures/ch04/poisson_bp.png" alt="SG · backpropagation · relative L₂ 0.0419"><figcaption>SG · backpropagation · relative L₂ 0.0419</figcaption></figure><figure class="figure"><img style="height:280px" src="/figures/ch04/poisson_global.png" alt="SG · global RFG · relative L₂ 0.0642"><figcaption>SG · global RFG · relative L₂ 0.0642</figcaption></figure><figure class="figure"><img style="height:280px" src="/figures/ch04/poisson_local.png" alt="SG · layerwise RFG · relative L₂ 0.0583"><figcaption>SG · layerwise RFG · relative L₂ 0.0583</figcaption></figure></div>
<div class="math-panel">

$$
-u_{xx}=f,\qquad \mathcal G_\theta:f\mapsto u,\qquad \varepsilon=\|\hat u-u\|_2/\|u\|_2
$$

</div>
<p class="protocol">Matched source Poisson panels · standard surrogate throughout · aggregate errors describe selected configurations, not seed uncertainty</p>
</div>

<!-- These are the matched source Poisson panels with the standard surrogate. The following table includes both SG and WSG configurations. -->

---
chapter: '4'
section: Randomized forward gradients · Accuracy
source: 'Thesis Chapter 4 · tab:rfg:poisson · Test relative L₂; SG = standard surrogate, WSG = weak surrogate; fig:rfg:convergence'
---

# Forward-mode training has an accuracy cost

<div class="density">
<div class="density-grid ">
<div class="detail-box"><h2>Poisson operator · test relative L₂</h2><table><thead><tr><th>Method</th><th>SG</th><th>WSG</th></tr></thead><tbody><tr><td>Backpropagation</td><td>0.0419</td><td>0.0394</td></tr><tr><td>Global RFG</td><td>0.0642</td><td>0.0637</td></tr><tr><td>Layerwise RFG</td><td>0.0583</td><td>0.0580</td></tr></tbody></table><p class="small">Layerwise estimates improve over global estimates here; backpropagation retains the lowest error.</p></div>
<figure class="figure"><img style="height:280px" src="/figures/ch04/convergence_rate.png" alt="Separate estimator study · convergence versus parameter dimension"><figcaption>Separate estimator study · convergence versus parameter dimension</figcaption></figure>
</div><p class="protocol">SG/WSG changes the spike derivative · global/layerwise changes parameter sampling · convergence figure is not the Poisson training curve</p>
</div>

<!-- Statistics are the selected source configurations, not an across-seed uncertainty estimate. Do not attribute the modest SG/WSG differences to a universal ranking. -->

---
chapter: '4'
section: Randomized forward gradients · Scaling limits
source: 'Thesis Chapter 4 · fig:rfg:box-large; fig:rfg:darcy · Published larger-scale comparisons; eq:rfg:darcy'
---

# Larger problems expose estimator limitations

<div class="density">
<div class="density-grid ">
<figure class="figure"><img style="height:290px" src="/figures/ch04/box_plot_deeponet_large.png" alt="Published operator-error distributions · BP / global / layerwise"><figcaption>Published operator-error distributions · BP / global / layerwise</figcaption></figure>
<div><div class="three"><figure class="figure"><img style="height:185px" src="/figures/ch04/darcy_bp.png" alt="BP"><figcaption>BP</figcaption></figure><figure class="figure"><img style="height:185px" src="/figures/ch04/darcy_global.png" alt="Global RFG"><figcaption>Global RFG</figcaption></figure><figure class="figure"><img style="height:185px" src="/figures/ch04/darcy_local.png" alt="Layerwise RFG"><figcaption>Layerwise RFG</figcaption></figure></div><div class="detail-box"><h2>Darcy solution operator</h2>
<div class="math-panel">

$$
-\nabla\!\cdot(a\nabla u)=f,\quad a\mapsto u
$$

</div>
<p class="small">Field structure and aggregate error can disagree; inspect both.</p></div></div>
</div><p class="protocol">Boxplots retain the source experiment distributions · larger parameter spaces challenge directional estimation · no hardware-cost inference</p>
</div>

<!-- Preserve the source distribution definitions and avoid translating this accuracy result into hardware energy savings. Transition: the second part changes the modeling question from spiking computation to inference from sparse data. -->
