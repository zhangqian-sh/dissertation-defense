---
chapter: '7'
section: Part II · Sequence-to-sequence modeling
source: 'Thesis Chapter 7 · Chapter overview'
divider: chapter
---

<p class="divider-chapter">Chapter 7</p>
<div class="divider-rule" aria-hidden="true"></div>

# OCFormer: Physics-Informed Transformers for High-Dimensional Optimal Control

<!-- Spoken transition: How to solve high-dimenstional optimal control problems with transformer-based model?

Move from field reconstruction to a separate optimal-control study. The trajectory model does not take reconstructed fields from the preceding experiments as inputs. -->

---
chapter: '7'
section: OCFormer · Control problem, PMP and latent dynamics
source: 'Thesis Chapter 7 · Abstract control problem, penalized PMP equations,
  decoupled Hamiltonian and straight-line latent solution'
---

# Optimal Control with Constraints

<div class="ocformer-pmp-layout ocformer-method-page">
<div>
<section>
<h3>Constrained optimal control</h3>

$$
\min_{x,u}\;\int_0^T\ell(x(t),u(t))\,dt+\Phi(x(0),x(T))
$$

$$
\begin{aligned}
\dot x(t)&=f(x(t),u(t)),\\
x(0)&\in X_0,\qquad x(T)\in X_T,\\
h(x(t))&\ge0,\qquad t\in[0,T].
\end{aligned}
$$

<p><InlineMath tex="x" /> is the joint state, <InlineMath tex="u" /> the control, <InlineMath tex="\ell" /> the running cost, and <InlineMath tex="\Phi" /> the endpoint cost. <InlineMath tex="h" /> collects inter-agent separation and obstacle-clearance constraints.</p>
</section>
<section class="ocformer-method-section">
<h3>Pontryagin's maximum principle (PMP)</h3>
<p>Add a smooth constraint penalty <InlineMath tex="U(h(x))" /> to the running cost. Maximize over the control to obtain the reduced Hamiltonian:</p>

$$
\begin{aligned}
H_0(x,p)&=\max_u\{p\cdot f(x,u)-\ell(x,u)\},\\
\bar H(x,p)&=H_0(x,p)-U(h(x)).
\end{aligned}
$$

$$
\dot x=\nabla_p\bar H,\qquad \dot p=-\nabla_x\bar H.
$$

<p>The costate <InlineMath tex="p" /> enters through PMP. For fixed endpoints, these equations define a coupled two-point boundary-value problem for the penalized objective.</p>
</section>
</div>
<div class="ocformer-latent-reference">
<section>
<h3>Intuition: a tractable latent system by temoving interactions</h3>
<p>For separable agent costs and dynamics, dropping <InlineMath tex="U" /> leaves a decoupled Hamiltonian <InlineMath tex="H_0" /> in latent coordinates <InlineMath tex="(y,q)" />.</p>

$$
\dot y=\nabla_q H_0(y,q),\qquad
\dot q=-\nabla_y H_0(y,q).
$$

<p>For <InlineMath tex="\dot x_i=u_i" /> and quadratic control effort:</p>

$$
H_0(y,q)=\tfrac12\|q\|^2,\qquad \dot y=q,\quad\dot q=0,
$$

$$
q=\frac{x^T-x^0}{T},\qquad y(t)=x^0+tq.
$$

<RecordedSequence name="latent" label="Latent and optimized trajectory time" caption="" />
<p>Straight latent motion provides a reference for the interacting physical trajectory. The next step is to parameterize its correction.</p>
</section>
</div>
</div>

<!--
The smooth PMP equations describe the penalized problem, not exact hard-state-constrained PMP. Removing U decouples agents for the separable costs and dynamics in this study. The animation uses saved optimized trajectories.
-->

---
chapter: '7'
section: OCFormer · Residual trajectory map and physics-informed training
source: 'Thesis Chapter 7 · Residual state–costate map, fig:oc:architecture, Hamiltonian residuals and endpoint matching'
---

# OCFormer: Learn the Trajectory Correction

<div class="ocformer-correction-layout ocformer-method-page">
<div>
<section>
<h3>Parameterize the state–costate trajectory</h3>

$$
(x_\theta,p_\theta)=\varphi_\theta(y,q)
=(y,q)+\Delta_\theta(y,q).
$$

<p>The known latent solution supplies <InlineMath tex="(y(t),q(t))" />. The network learns the displacement and costate correction required by interactions.</p>
</section>
<section class="ocformer-method-section">
<h3>Network structure</h3>
<figure class="figure"><img src="/figures/ch07/ocformer-architecture.png" alt="Agent-token embeddings, alternating attention updates and residual connections map latent states and costates to physical states and costates"></figure>
<p>Each agent is a token. Self-attention couples agents; alternating updates act on the two streams, and identity skips implement the residual map.</p>
<p>The inverse-map interpretation assumes a diffeomorphism; invertibility and symplecticity are not enforced by the network.</p>
</section>
</div>
<div>
<section>
<h3>Enforce the full Hamiltonian equations</h3>
<p>Evaluate the map at collocation times <InlineMath tex="t_j" /> and differentiate through it along the latent trajectory:</p>

$$
\begin{aligned}
r_x(t)&=\dot x_\theta(t)-\nabla_p\bar H(x_\theta(t),p_\theta(t)),\\
r_p(t)&=\dot p_\theta(t)+\nabla_x\bar H(x_\theta(t),p_\theta(t)).
\end{aligned}
$$

$$
\mathcal L_{\mathrm{PMP}}=\frac1N\sum_{j=1}^{N}
\bigl(\|r_x(t_j)\|^2+\|r_p(t_j)\|^2\bigr).
$$

</section>
<section class="ocformer-method-section">
<h3>Match endpoints and train the correction</h3>

$$
\mathcal L_{\mathrm{bdry}}=
\|x_\theta(0)-x^0\|^2+\|x_\theta(T)-x^T\|^2,
$$

$$
\mathcal L=\mathcal L_{\mathrm{PMP}}
+\lambda_{\mathrm{bdry}}\mathcal L_{\mathrm{bdry}}
+\mathcal L_{\mathrm{aux}}.
$$

<p>The collision and obstacle penalty remains inside <InlineMath tex="\bar H" />; benchmark-specific auxiliary losses can add velocity and constraint terms.</p>
<p>Optimize with Adam, then L-BFGS, using boundary data and collocation times rather than labeled optimal trajectories.</p>
</section>
</div>
</div>

<!-- L_aux denotes the aggregate of benchmark-specific auxiliary terms and their weights. Hamiltonian residuals are necessary-condition targets for the penalized problem; finite loss does not certify global optimality or continuous-time feasibility. -->

---
chapter: '7'
section: OCFormer · Baseline scaling
source: 'Thesis Chapter 7 · tab:oc:sympocnet; tab:oc:2d-scaling · 2D antipodal
  configurations'
---

# Example: Drones in 2d room

<div class="ocformer-scaling-layout">
<div><SwarmScaling /></div>
<div class="ocformer-scaling-results">
<h3>2D antipodal configurations</h3>
<p>Drones move to antipodal targets over <InlineMath tex="T=10" /> without collision.</p>
<table>
<colgroup><col style="width:9%"><col style="width:21%"><col style="width:24%"><col style="width:22%"><col style="width:24%"></colgroup>
<thead><tr><th><InlineMath tex="M" /></th><th>OCFormer cost</th><th>SympOCNet cost</th><th>Lower bound gap</th><th>Minimum clearance</th></tr></thead>
<tbody>
<tr><td>8</td><td>0.4036</td><td>0.4046</td><td>0.9%</td><td><InlineMath tex="1.5\times10^{-4}" /></td></tr>
<tr><td>16</td><td>0.8307</td><td>0.8345</td><td>3.8%</td><td><InlineMath tex="1.5\times10^{-4}" /></td></tr>
<tr><td>32</td><td>1.2531</td><td>1.4413</td><td>8.4%</td><td><InlineMath tex="1.5\times10^{-4}" /></td></tr>
<tr><td>128</td><td>5.1424</td><td>Infeasible</td><td>9.3%</td><td><InlineMath tex="1.2\times10^{-4}" /></td></tr>
</tbody>
</table>
<p>Lower bound gap is relative to unconstrained optimal control. At 32 agents, OCFormer lowers cost by approximately 13%.</p>
<p>Drones radius: 0.02 for 8/16/32; 0.01 for 128.</p>
</div>
</div>

<!--
Merged existing comparison and scaling tables by M, preserving all five rows including M=4. The four native canvas animations use saved best_pred_lbfgs trajectories for M=8/16/32/128; they do not recompute or certify the table's 5000-time clearance results.
-->

---
chapter: '7'
section: OCFormer · Boundary-condition perturbations
source: 'Thesis Chapter 7 · Frozen-backbone transfer; archived 8/16-agent perturbation trajectories and boundary_0000 training logs'
---

# Perturb Initial and Terminal Conditions

<div class="ocformer-transfer-layout ocformer-method-page">
<div>
<section>
<h3>New endpoints, the same control problem</h3>

$$
x(0)=x^0+\delta_0,\qquad x(T)=x^T+\delta_T.
$$

<p>A small change to the boundary data changes the whole interacting trajectory. Independently displaced agents cannot generally be matched by one rigid transformation.</p>
</section>
<section class="ocformer-method-section">
<h3>Adapt the map, retain the backbone</h3>

$$
\varphi_{\mathrm{new}}
=\mathcal W_{\mathrm{fwd}}\circ\varphi_{\theta^*}
\circ\mathcal W_{\mathrm{inv}}.
$$

<p>Freeze the trained OCFormer. Fit lightweight affine wrappers and bounded per-agent corrections using the Hamiltonian residuals and the new endpoint loss.</p>
</section>
<section class="ocformer-method-section">
<h3>Transfer across swarm sizes</h3>
<p>The two recorded cases perturb initial positions while keeping terminal targets fixed: <InlineMath tex="\delta_T=0" />. Fit the wrappers separately for each boundary configuration. These are fine-tuned transfer results, not amortized inference.</p>
</section>
</div>
<div class="ocformer-transfer-results">
<OCFormerExamples mode="perturbation" />
<section class="ocformer-transfer-metrics">
<h3>Fine-tuned transfer results</h3>
<table>
<colgroup><col style="width:8%"><col style="width:20%"><col style="width:17%"><col style="width:28%"><col style="width:27%"></colgroup>
<thead><tr><th><InlineMath tex="M" /></th><th>Max. shift</th><th>Cost</th><th>Min. clearance</th><th>Fine-tuning time</th></tr></thead>
<tbody>
<tr><td>8</td><td>0.0381</td><td>0.4130</td><td><InlineMath tex="-4.15\times10^{-4}" /></td><td>44.6 s</td></tr>
<tr><td>16</td><td>0.0388</td><td>0.8277</td><td><InlineMath tex="8.29\times10^{-5}" /></td><td>42.9 s</td></tr>
</tbody>
</table>
<p>Max. shift is <InlineMath tex="\|\delta_0\|_\infty" />. Clearance is sampled at 200 times; negative values indicate overlap. Time includes both optimizers and startup.</p>
</section>
</div>
</div>

---
chapter: '7'
section: OCFormer · Three-dimensional obstacle navigation
source: 'Archived room_3d positional mean and ball_3d M16 trajectories; boundary
  data in data/ball_3d/n=16'
---

# Example: Drones in 3d room

<OCFormerExamples mode="three-d" />

<!--
ch7-34 metrics: boundary_0000 best_pred_lbfgs; final training-log cost/constraint, Adam plus L-BFGS elapsed time. 8: 29.88+14.71 s; 16: 30.14+12.78 s. Max. shifts measured from boundary minus reference.
-->
