---
chapter: '4'
section: Randomized forward gradients · Method
source: 'Thesis Chapter 4 · sec:rfg:estimator; eq:rfg:directional; eq:rfg:global; eq:rfg:layerwise'
---

# Train with directional derivatives in forward mode

$$
d_{\mathbf v}=\nabla_\theta\mathcal L(\theta)^\top\mathbf v,
\qquad \widehat{\mathbf g}=d_{\mathbf v}\,\mathbf v
$$

<div class="flow"><div><strong>Sample a direction</strong><br><span class="small">Random parameter perturbation v</span></div><span class="arrow">→</span><div><strong>Carry a JVP forward</strong><br><span class="small">A directional derivative of the loss</span></div><span class="arrow">→</span><div><strong>Form an estimator</strong><br><span class="small">Use the direction and its derivative</span></div></div>
<div class="cols"><div class="rule"><h2>Global sampling</h2><p class="small">One direction spans all trainable parameters.</p></div><div class="rule"><h2>Layerwise sampling</h2><p class="small">Perturbations are organized by layer to control estimator quality.</p></div></div>
<p class="micro" style="margin-top:20px">RFG avoids reverse mode, not derivatives. Parameter sampling and weak-surrogate threshold noise are distinct.</p>

<!-- Source experiments describe Bernoulli parameter perturbations. Gaussian threshold shifts belong to the weak surrogate, not the same sampling operation. No measured training-energy savings are claimed. -->

---
chapter: '4'
section: Randomized forward gradients · Matched predictions
source: 'Thesis Chapter 4 · fig:rfg:poisson · Standard surrogate-gradient configurations'
---

# Matched Poisson predictions across training methods

<div class="three" style="margin-top:24px"><figure class="figure"><img src="/figures/ch04/poisson_bp.png" alt="Poisson operator reference and BP prediction"><figcaption>Backpropagation · SG-BP</figcaption></figure><figure class="figure"><img src="/figures/ch04/poisson_global.png" alt="Poisson operator reference and global RFG prediction"><figcaption>Global RFG · SG-RFG-G</figcaption></figure><figure class="figure"><img src="/figures/ch04/poisson_local.png" alt="Poisson operator reference and layerwise RFG prediction"><figcaption>Layerwise RFG · SG-RFG-L</figcaption></figure></div>
<div class="takeaway">Compare the predicted functions as well as the aggregate errors.</div>

<!-- These are the matched source Poisson panels with the standard surrogate. The following table includes both SG and WSG configurations. -->

---
chapter: '4'
section: Randomized forward gradients · Accuracy
source: 'Thesis Chapter 4 · tab:rfg:poisson · Test relative L₂; SG = standard surrogate, WSG = weak surrogate'
---

# Forward-mode training has an accuracy cost

<div class="cols" style="margin-top:25px">
<table><thead><tr><th>Method</th><th>SG</th><th>WSG</th></tr></thead><tbody><tr class="highlight"><td>Backpropagation</td><td>0.0419</td><td>0.0394</td></tr><tr><td>RFG · global</td><td>0.0642</td><td>0.0637</td></tr><tr><td>RFG · layerwise</td><td>0.0583</td><td>0.0580</td></tr></tbody></table>
<div class="rule"><h2>One-dimensional Poisson operator</h2><p class="small">Both RFG variants learn useful predictions.</p><p class="small">Layerwise sampling improves over global sampling in these reported configurations.</p><p class="small">Backpropagation retains the lowest error.</p></div>
</div>
<div class="takeaway">The evidence supports a computational alternative with a measurable accuracy trade-off.</div>

<!-- Statistics are the selected source configurations, not an across-seed uncertainty estimate. Do not attribute the modest SG/WSG differences to a universal ranking. -->

---
chapter: '4'
section: Randomized forward gradients · Scaling limits
source: 'Thesis Chapter 4 · fig:rfg:box-large; fig:rfg:darcy · Published larger-scale comparisons'
---

# Larger problems expose estimator limitations

<div class="cols wide-left" style="margin-top:16px">
<figure class="figure tall"><img src="/figures/ch04/box_plot_deeponet_large.png" alt="Error distributions for larger operator learning experiments"><figcaption>Published BP, global-RFG and layerwise-RFG error distributions.</figcaption></figure>
<div><div class="three" style="gap:8px"><figure class="figure short"><img src="/figures/ch04/darcy_bp.png" alt="Darcy BP prediction"><figcaption>BP</figcaption></figure><figure class="figure short"><img src="/figures/ch04/darcy_global.png" alt="Darcy global RFG prediction"><figcaption>Global</figcaption></figure><figure class="figure short"><img src="/figures/ch04/darcy_local.png" alt="Darcy layerwise RFG prediction"><figcaption>Layerwise</figcaption></figure></div><p class="small" style="margin-top:18px">Useful field structure can coexist with a wider error distribution.</p></div>
</div>

<!-- Preserve the source distribution definitions and avoid translating this accuracy result into hardware energy savings. Transition: the second part changes the modeling question from spiking computation to inference from sparse data. -->
