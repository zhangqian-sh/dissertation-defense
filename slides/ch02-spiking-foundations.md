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
section: Spiking representations · Spiking neurons
source: 'Illustrative leaky integrate-and-fire neuron · Concept adapted from data/references/flowchart/snn.png'
---

# How spiking neural networks work

<SpikingNeuronIntro />

<!-- Schematic, not experimental data. The trace uses beta=0.90, threshold=1, weight=0.60 and instantaneous reset to zero after a threshold crossing. u denotes voltage before reset; v denotes voltage after reset. This introductory model is distinct from the delayed-reset implementation discussed on the SMS method slide. -->

---
chapter: '2'
section: Spiking representations · Encoding
source: 'Thesis Chapter 2 · Magnitude-prefix encoding and mean decoding · Regenerated illustrative example, K=40'
---

# From continuous functions to spikes

<div class="encoding-overview">
<section class="encoding-methods">
<h2>Encoding methods</h2>
<p>Normalize the coordinate to <InlineMath tex="a\in[0,1]" />.</p>
<CoordinateEncodings layout="column" />
<p class="encoding-method-key">Brown cells denote spikes; rasters use 8 schematic steps.</p>
</section>

<div class="encoding-cycle">
<h2 class="encoding-example-heading">Encoding and decoding · Ours</h2>
<div class="encoding-annotation">
<div class="encoding-rule"><h2>Encoding</h2><div>

$a_j=\dfrac{f(x_j)-z_{\min}}{z_{\max}-z_{\min}},\qquad N_j=\lfloor Ka_j\rfloor,\qquad s_j[k]=\mathbf{1}_{k\leq N_j}$

</div></div>
</div>
<svg class="encoding-arrow" viewBox="0 0 1000 48" aria-label="Encoding: continuous values to discrete spikes"><path d="M240 48 C350 0 642.668 -3.200 752.668 44.800" /><polygon points="760.000,48.000 749.235,47.667 752.434,40.334" class="encoding-arrowhead" /></svg>
<div class="encoding-figures">
<figure>
<figcaption>

Continuous values $f(x)$

</figcaption><img src="/figures/ch02/encoding_continuous_compact.svg" alt="Continuous field and decoded samples, with spatial position x increasing from left to right"></figure>
<figure>
<figcaption>

Discrete spike image $s_j[k]\in\{0,1\}$

</figcaption><img src="/figures/ch02/encoding_discrete_compact.svg" alt="Binary prefix spikes: the same spatial position x runs left to right; spike step k increases upward"><p class="encoding-key"><i></i> Spike = 1 <i class="silent"></i> No spike = 0</p></figure>
</div>
<svg class="encoding-arrow" viewBox="0 0 1000 48" aria-label="Decoding: discrete spikes back to continuous values"><path d="M760 0 C650 48 357.332 51.200 247.332 3.200" /><polygon points="240.000,0.000 250.765,0.333 247.566,7.666" class="encoding-arrowhead" /></svg>
<div class="encoding-annotation">
<div class="encoding-rule"><h2>Decoding</h2><div>

$\begin{gathered}\hat f(x_j)=z_{\min}+\dfrac{z_{\max}-z_{\min}}{K}\sum_{k=1}^{K}s_j[k],\\[3pt]0\le f(x_j)-\hat f(x_j)<\dfrac{z_{\max}-z_{\min}}{K}\end{gathered}$

</div></div>
</div>
<div class="encoding-note">

Illustrative magnitude encoding · $K=40$ · $[z_{\min},z_{\max}]=[0,0.2]$. Resolution $\Delta f=0.005$. Spike step $k$ is internal simulation time, not physical time.

</div>
</div>
</div>

<!-- Both figures are generated from the same analytic example by scripts/prepare_encoding_figure.py. This is magnitude-prefix encoding, not the separate grid-index encoding of coordinates. The dashed decoded field illustrates the finite-K quantization error. -->

---
chapter: '2'
section: Spiking representations · Operator accuracy
source: 'Thesis Chapter 2 · tab:ch02:deeponet-encoding; fig:snn:deeponet-poisson · Savitzky–Golay window 51, order 3'
---

# Example: DeepONet for 1d Poisson equation

<div class="poisson-example poisson-example-results">
<div class="poisson-column">
<section class="poisson-section">
<h2>Problem setup</h2>

$$
-u''(x)=f(x),\quad x\in(0,1),\qquad u(0)=u(1)=0
$$

<div class="poisson-prose">

Learn the solution operator $\mathcal G_\theta:f\mapsto u$.

</div>
<p class="poisson-context">GRF forcing · 800 training / 200 test pairs · 100 spatial points.</p>
</section>
<PoissonDeepONetDiagram />

</div>
<div class="poisson-column">

<section class="poisson-section poisson-evaluation">
<div class="poisson-metric"><h2>Relative L₂ error</h2><div>

$\varepsilon_{L_2}=\dfrac{\|\hat u-u\|_2}{\|u\|_2}$

</div></div>

<table><thead><tr><th>Encoding</th><th>K</th><th>Mean</th><th>Std.</th></tr></thead><tbody><tr><td>Rate</td><td>50</td><td>0.229</td><td>0.174</td></tr><tr><td>Direct</td><td>50</td><td>0.135</td><td>0.067</td></tr><tr class="poisson-ours"><td>Ours</td><td>50</td><td>0.047</td><td>0.032</td></tr><tr><td>Ours</td><td>500</td><td>0.005</td><td>0.003</td></tr></tbody></table>
<p class="poisson-context">Mean and standard deviation across test cases; predictions smoothed with Savitzky–Golay (window 51, order 3).</p>
</section>
</div>
<figure class="poisson-prediction">
<div class="poisson-prediction-image"><img src="/figures/ch02/deeponet_poisson_triangular_long.png" alt="Four published Poisson solution examples in a horizontal row, using Ours at K=500"></div>
<figcaption>

Four examples · Ours, $K=500$.

</figcaption>
</figure>
</div>

<!-- Encoding methods are introduced on the preceding slide. All four published K=500 prediction panels and every reported table value are preserved. Direct is the learned dense/spiking encoder selected by run_deeponet_1d.py, not a one-hot latency code. -->

---
chapter: '2'
section: Spiking marching scheme · Method
source: 'Thesis Chapter 2 · eq:ch02:sms-update; fig:snn:sms-workflow; fig:snn:sms-architecture'
---

# Spiking marching scheme

<script setup>
import SMSMethodDiagram from "/components/SMSMethodDiagram.vue"
</script>

<div class="sms-method">
<div class="sms-method-left">

<SMSMethodDiagram />

<div class="sms-lif">
<h2>LIF · Leaky integrate-and-fire</h2>
<p>Membrane voltage accumulates incoming spikes, leaks, and resets after firing.</p>

$$
\begin{aligned}
V_k&=(\beta V_{k-1}+s_k)(1-z_{k-1}),\\
z_k&=\mathbf1_{V_k>V_{\mathrm{th}}}.
\end{aligned}
$$

$\beta$: voltage retention; $V_{\mathrm{th}}$: threshold; $s_k$: input spikes; $z_k$: emitted spikes.

</div>

<div class="sms-training"><strong>Training</strong><p>Numerical solvers provide ground truth. Use crossentropy between predicted and true spike to train, like binary image matching.</p></div>
<div class="sms-time-note">

Physical step $n$ advances the solution; $k=1,\ldots,K$ indexes spike steps.

</div>
</div>
<div class="sms-method-right">
<div class="sms-algorithm">
<div class="sms-algorithm-heading"><strong>Algorithm 1</strong><span>Autoregressive</span></div>
<div class="sms-algorithm-io">

**Input:** initial states $u^0,u^1$; trained SNN.<br>
**Output:** predicted trajectory $\{\hat u^n\}_{n=0}^{N}$.

</div>
<ol>
<li>

$\hat s^0\gets\mathcal E(u^0),\quad \hat s^1\gets\mathcal E(u^1)$

</li>
<li>

**for** $n=1,\ldots,N-1$ **do**

</li>
<li class="sms-indent">

$\hat s^{n+1}\gets H[\mathrm{SNN}(\hat s^{n-1},\hat s^n)]$

</li>
<li><strong>end for</strong></li>
<li>

Decode outputs: $\hat u^n\gets\mathcal D(\hat s^n)$.

</li>
</ol>
</div>

<div class="sms-algorithm">
<div class="sms-algorithm-heading"><strong>Algorithm 2</strong><span>Teacher-forced</span></div>
<div class="sms-algorithm-io">

**Input:** reference trajectory $\{u^n\}_{n=0}^{N}$; trained SNN.<br>
**Output:** predictions $\{\hat u^n\}_{n=2}^{N}$.

</div>
<ol>
<li>

$s^n\gets\mathcal E(u^n),\quad n=0,\ldots,N-1$

</li>
<li>

**for** $n=1,\ldots,N-1$ **do**

</li>
<li class="sms-indent">

$\hat s^{n+1}\gets H[\mathrm{SNN}(s^{n-1},s^n)]$

</li>
<li><strong>end for</strong></li>
<li>

Decode outputs: $\hat u^n\gets\mathcal D(\hat s^n)$.

</li>
</ol>
</div>
</div>
</div>

<!-- The spike rasters in SMSMethodDiagram are schematic, not benchmark predictions. The spike-space cascade follows spiking_marching_scheme/src/evaluate.py; main.py decodes the completed output trajectory. The LIF recurrence matches src/nn/sequential/layer.py: reset gates the next voltage update. Distinguish physical marching step n from internal encoding step k. -->

---
chapter: '2'
section: Spiking marching scheme · Temporal inspection
source: 'Thesis Chapter 2 · fig:snn:pde-heat · Saved heat run, K=100; unsmoothed relative L₂ on 101 nodes'
---

# Example: Heat equation

<SMSRollout />

<div style="font-size:14px;margin-top:10px;line-height:1.5">
<h2 style="font-size:16px;margin-bottom:6px">Problem setup</h2>

$u_t=\alpha u_{xx},\quad x\in[0,1],\quad\alpha=1.$

$K=100$ · 101 spatial nodes · $\Delta t_{\mathrm{SMS}}=4\times10^{-4}\,\mathrm{s}$.

</div>

<!-- Demo: start at t=0 s; play through the training marker at 0.032 s and inspect the growing relative error. Initial two frames are encoded reference histories. No stability theorem is inferred from this case. -->
