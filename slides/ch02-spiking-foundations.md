---
chapter: '2'
section: Part I · Neuromorphic algorithms
source: 'Thesis Chapter 2 · Chapter overview'
divider: part
---

<div class="eyebrow">Part I · Neuromorphic algorithms</div>
<p class="divider-chapter">Chapter 2</p>
<div class="divider-rule" aria-hidden="true"></div>

# Exploratory Studies on Spiking Representations

<!-- Spoken transition: Setup: How to represent continuous values with spikes?

Begin Part I with representation: how continuous quantities become spikes, then how those representations support operator evaluation and physical-time marching. -->

---
chapter: '2'
section: Spiking representations · Encoding
source: 'Thesis Chapter 2 · fig:snn:encoding · Lower-triangular encoding, K=30'
---

# From a continuous field to a spike representation

<p class="subtitle">The encoding determines which numerical structure survives discretization.</p>
<div class="cols">
<figure class="figure"><img src="/figures/ch02/encoding_function.png" alt="Continuous field used in the encoding example"><figcaption>Continuous input field on a spatial grid.</figcaption></figure>
<figure class="figure"><img src="/figures/ch02/encoding_spike_raster.png" alt="Lower triangular encoding spike raster"><figcaption>Lower-triangular spike raster; internal horizon K = 30.</figcaption></figure>
</div>
<div class="takeaway">An ordered prefix code represents magnitude through spike count. Finite K introduces a resolution–cost trade-off.</div>

<!-- Physical coordinates and internal spike time are different axes. This example demonstrates the encoding; its raster is not a physical-time trajectory. -->

---
chapter: '2'
section: Spiking representations · Operator accuracy
source: 'Thesis Chapter 2 · tab:ch02:deeponet-encoding; fig:snn:deeponet-poisson · Savitzky–Golay window 51, order 3'
---

# Encoding changes Poisson operator accuracy

<p class="subtitle">Relative discrete L₂ error over 200 held-out samples, after smoothing.</p>
<div class="cols wide-left">
<table><thead><tr><th>Trunk encoding</th><th>K</th><th>Mean</th><th>Std.</th></tr></thead><tbody>
<tr><td>Rate</td><td>50</td><td>0.229</td><td>0.174</td></tr>
<tr><td>Floating point</td><td>50</td><td>0.692</td><td>0.451</td></tr>
<tr><td>Direct</td><td>50</td><td>0.135</td><td>0.067</td></tr>
<tr class="highlight"><td>Lower triangular</td><td>50</td><td>0.047</td><td>0.032</td></tr>
<tr class="highlight"><td>Lower triangular</td><td>500</td><td>0.005</td><td>0.003</td></tr>
</tbody></table>
<div><figure class="figure short"><img src="/figures/ch02/deeponet_poisson_triangular_long.png" alt="Poisson forcing and solution with lower triangular encoding K500"><figcaption>Published Poisson solution example, K = 500.</figcaption></figure><p class="small" style="margin-top:15px">The reported errors concern the <strong>operator prediction</strong>, not scalar encoding alone.</p></div>
</div>

<!-- Read these statistics with the smoothing qualification. Standard deviation is across held-out samples. Increasing K by ten improves accuracy here but also multiplies internal simulation steps. Only one example field is shown; do not imply unmatched source panels use the same forcing. -->

---
chapter: '2'
section: Spiking marching scheme · Method
source: 'Thesis Chapter 2 · eq:ch02:sms-update; fig:snn:sms-workflow'
---

# Learn a time-step map in spike space

<div class="cols wide-right" style="margin-top:22px">
<div><h2>Spiking Marching Scheme</h2><p class="small">Encode a state history, predict the next encoded state, and decode a numerical field.</p><div class="rule" style="margin-top:24px"><h3>Two evaluation protocols</h3><p class="small"><strong>Reference-fed:</strong> each prediction receives the reference history.</p><p class="small"><strong>Cascade:</strong> predictions become the next input history.</p></div></div>
<figure class="figure tall"><img src="/figures/ch02/sms_workflow.png" alt="Spiking Marching Scheme training and recursive prediction workflow"><figcaption>Source workflow. Recursive evaluation tests accumulated error.</figcaption></figure>
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
