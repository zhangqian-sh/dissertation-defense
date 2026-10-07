---
chapter: '2'
section: Part I · Neuromorphic algorithms
source: 'Thesis Chapter 2 · Chapter overview'
divider: part
---

<p class="divider-chapter">Chapter 2</p>
<div class="divider-rule" aria-hidden="true"></div>

# Exploratory Studies on Spiking Representations

<!-- Spoken transition: Setup: How to represent continuous values with spikes?

Begin Part I with representation: how continuous quantities become spikes, then how those representations support operator evaluation and physical-time marching. -->

---
chapter: '2'
section: Spiking representations · Encoding
source: 'Thesis Chapter 2 · fig:snn:encoding · Lower-triangular encoding, K=30; eq:ch02:triangular-value; eq:ch02:triangular-grid; eq:ch02:decode-mean'
---

# From a continuous field to a spike representation

<div class="density">
<div class="density-grid ">
<figure class="figure"><img style="height:185px" src="/figures/ch02/encoding_function.png" alt="Continuous field · spatial coordinate"><figcaption>Continuous field · spatial coordinate</figcaption></figure>
<figure class="figure"><img style="height:185px" src="/figures/ch02/encoding_spike_raster.png" alt="Prefix spikes · internal horizon K = 30"><figcaption>Prefix spikes · internal horizon K = 30</figcaption></figure>
</div><div class="density-grid ">
<div class="detail-box"><h2>Encode a normalized magnitude</h2>
<div class="math-panel">

$$
\begin{aligned}a&=\frac{f-z_{\min}}{z_{\max}-z_{\min}},\quad N=\lfloor Ka\rfloor\\s[k]&=\mathbf1_{k\le N}\end{aligned}
$$

</div>
<p class="small">Each value becomes a prefix of N spikes; k is internal simulation time.</p></div>
<div class="detail-box"><h2>Decode and resolve</h2>
<div class="math-panel">

$$
\hat a=\frac1K\sum_{k=1}^{K}s[k],\qquad \Delta f=\frac{z_{\max}-z_{\min}}K
$$

</div>
<p class="small">Spatial coordinates use a grid-index prefix; state values use normalized magnitude.</p></div>
</div>
</div>

<!-- Physical coordinates and internal spike time are different axes. This example demonstrates the encoding; its raster is not a physical-time trajectory. -->

---
chapter: '2'
section: Spiking representations · Operator accuracy
source: 'Thesis Chapter 2 · tab:ch02:deeponet-encoding; fig:snn:deeponet-poisson · Savitzky–Golay window 51, order 3'
---

# Encoding changes Poisson operator accuracy

<div class="density">
<div class="density-grid ">
<table><thead><tr><th>Trunk encoding</th><th>K</th><th>Mean</th><th>Std.</th></tr></thead><tbody><tr><td>Rate</td><td>50</td><td>0.229</td><td>0.174</td></tr><tr><td>Floating point</td><td>50</td><td>0.692</td><td>0.451</td></tr><tr><td>Direct</td><td>50</td><td>0.135</td><td>0.067</td></tr><tr><td>Lower triangular</td><td>50</td><td>0.047</td><td>0.032</td></tr><tr><td>Lower triangular</td><td>500</td><td>0.005</td><td>0.003</td></tr></tbody></table>
<figure class="figure"><img style="height:230px" src="/figures/ch02/deeponet_poisson_triangular_long.png" alt="Published forcing/solution example · K = 500"><figcaption>Published forcing/solution example · K = 500</figcaption></figure>
</div><div class="density-grid ">
<div class="detail-box"><h2>Learn a solution operator</h2>
<div class="math-panel">

$$
-u_{xx}=f,\qquad \mathcal G_\theta:f\mapsto u
$$

</div>
</div>
<div class="detail-box"><h2>Evaluate the decoded field</h2>
<div class="math-panel">

$$
\varepsilon_{L_2}=\frac{\|\hat u-u\|_2}{\|u\|_2}
$$

</div>
<p class="small">Tenfold K improves reported mean error from 0.047 to 0.005; it also increases internal steps.</p></div>
</div><p class="protocol">800 train / 200 held-out · 100 spatial points · mean and SD · Savitzky–Golay window 51, order 3 · operator error after smoothing</p>
</div>

<!-- Read these statistics with the smoothing qualification. Standard deviation is across held-out samples. Increasing K by ten improves accuracy here but also multiplies internal simulation steps. Only one example field is shown; do not imply unmatched source panels use the same forcing. -->

---
chapter: '2'
section: Spiking marching scheme · Method
source: 'Thesis Chapter 2 · eq:ch02:sms-update; fig:snn:sms-workflow; fig:snn:sms-architecture'
---

# Learn a time-step map in spike space

<div class="density">

<div class="math-panel">

$$
\hat u^{n+1}=\mathcal D\!\left[\mathrm{SNN}_\theta\!\left(\mathcal E(u^{n-1},u^n)\right)\right]
$$

</div>
<div class="density-grid ">
<figure class="figure"><img style="height:220px" src="/figures/ch02/sms_workflow.png" alt="Encode history → predict spikes → decode → feed back"><figcaption>Encode history → predict spikes → decode → feed back</figcaption></figure>
<div class="detail-box"><h2>Train and evaluate the same map</h2><p class="small"><strong>Architecture:</strong> LIF layer → two ReLU dense layers; hidden width 500.</p><p class="small"><strong>Training:</strong> classical-integrator pairs; sigmoid cross-entropy on spike targets.</p><p class="small"><strong>Reference-fed:</strong> use true histories at every step.</p><p class="small"><strong>Cascade:</strong> decoded predictions replace the next history.</p></div>
</div><p class="protocol">Physical step n advances the PDE/ODE · spike step k = 1,…,K encodes each state · cascade tests accumulated error</p>
</div>

<!-- The same learned one-step map is evaluated with different input histories. The next slide uses the heat benchmark and retains the initial encoded histories. -->

---
chapter: '2'
section: Spiking marching scheme · Temporal inspection
source: 'Thesis Chapter 2 · fig:snn:pde-heat · Saved heat run, K=100; unsmoothed relative L₂ on 101 nodes'
---

# Recursive error beyond the training interval

<SMSRollout />

<!-- Demo: start at t=0 s; play through the training marker at 0.032 s and inspect the growing relative error. Initial two frames are encoded reference histories. No stability theorem is inferred from this case. -->
