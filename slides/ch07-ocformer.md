---
chapter: '7'
section: Chapter 7 · Transition
source: 'Thesis Chapter 7 · Chapter overview'
divider: chapter
---

<div class="eyebrow">Chapter 7</div>
<div class="divider-rule" aria-hidden="true"></div>

# OCFormer: Physics-Informed Transformers for High-Dimensional Optimal Control

<!-- Spoken transition: How to solve high-dimenstional optimal control problems with transformer-based model?

Move from field reconstruction to a separate optimal-control study. The trajectory model does not take reconstructed fields from the preceding experiments as inputs. -->

---
chapter: '7'
section: OCFormer · Optimal-control formulation
source: 'Thesis Chapter 7 · Problem formulation and Hamiltonian system'
---

# Coordinated motion under coupled constraints

<div class="density">
<div class="density-grid ">
<div class="detail-box"><h2>Single-integrator benchmarks</h2>
<div class="math-panel">

$$
\min_{x,u}\ J=\int_0^T\frac12\sum_{i=1}^{M}\|u_i(t)\|^2\,dt
$$

</div>

<div class="math-panel">

$$
\dot x_i=u_i,\qquad x_i(0)=x_i^0,\quad x_i(T)=x_i^T
$$

</div>
<p class="small">Joint state dimension Md; interaction constraints couple otherwise independent agents.</p></div>
<div class="detail-box"><h2>Geometry and feasibility</h2><svg class="geometry-sketch" viewBox="0 0 430 165" role="img" aria-label="Schematic of two agents crossing from initial to terminal positions with a central obstacle"><rect x="15" y="12" width="400" height="140" fill="#f6f5f4" stroke="#98A4AE"/><circle cx="215" cy="82" r="29" fill="#dce1df" stroke="#596361"/><path d="M55 50 Q215 -15 375 113" fill="none" stroke="#4E3629" stroke-width="3"/><path d="M55 113 Q215 185 375 50" fill="none" stroke="#ED1C24" stroke-width="3"/><g fill="white" stroke="#4E3629" stroke-width="3"><circle cx="55" cy="50" r="7"/><circle cx="55" cy="113" r="7"/></g><g fill="#4E3629"><rect x="369" y="107" width="12" height="12"/><rect x="369" y="44" width="12" height="12"/></g><text x="27" y="33">Initial</text><text x="345" y="33">Terminal</text><text x="179" y="87">Obstacle</text></svg>
<div class="math-panel">

$$
\begin{aligned}h_{ij}(x)&=\|x_i-x_j\|-2r_{agent}\ge0\\h_{ball}(x)&=\|x_i-c\|-R_{excl}\ge0\end{aligned}
$$

</div>
<p class="small">Ball obstacle: center c, agent-center exclusion radius R_excl. Other geometries use their signed clearance; sketch is conceptual.</p></div>
</div><p class="protocol">2D antipodal benchmark: T = 10 · agent radii 0.01 or 0.02 by configuration · trajectory cost and feasibility are separate outcomes</p>
</div>

<!-- This is a separate optimal-control study. Do not imply its input fields came from the reconstruction models. -->

---
chapter: '7'
section: OCFormer · Latent and physical coordinates
source: 'Thesis Chapter 7 · fig:oc:latent-physical; fig:oc:architecture · State–costate transformation'
---

# Learn a map from latent to physical trajectories

<div class="cols" style="margin-top:15px"><RecordedSequence name="latent" label="Latent and optimized trajectory time" caption="Left: straight endpoint reference. Right: saved L-BFGS optimized trajectories from the paper’s run; not a hand-designed detour." /><div><figure class="figure"><img src="/figures/ch07/ocformer-architecture.png" alt="OCFormer attention based transformation architecture"><figcaption>Attention-based architecture for interacting agents.</figcaption></figure>
<div class="math-panel">

$$
\begin{aligned}(x_\theta,p_\theta)&=\varphi_\theta(y,q)\\y(t)&=x^0+tq,\quad q=(x^T-x^0)/T\end{aligned}
$$

</div></div></div>
<div class="takeaway">Learned inverse-map ansatz; diffeomorphism remains an assumption. OCFormer does not enforce symplecticity.</div>

<!-- OCFormer is permutation-equivariant, not asserted symplectic. The latent-map motivation includes a diffeomorphism assumption; preserve that distinction. -->

---
chapter: '7'
section: OCFormer · Physics-informed training
source: 'Thesis Chapter 7 · fig:oc:training · Hamiltonian residuals and boundary matching; eq:oc:loss'
---

# Train the trajectory map with physics and boundaries

<div class="density">
<div class="density-grid ">
<figure class="figure"><img style="height:285px" src="/figures/ch07/training-flowchart.png" alt="Latent boundary data → state–costate map → automatic differentiation"><figcaption>Latent boundary data → state–costate map → automatic differentiation</figcaption></figure>
<div class="detail-box"><h2>Residuals and endpoint matching</h2>
<div class="math-panel">

$$
r_x=\dot x_\theta-\nabla_p\bar H,\qquad r_p=\dot p_\theta+\nabla_x\bar H
$$

</div>

<div class="math-panel">

$$
\mathcal L_{PINN}=\frac1N\sum_i(\|r_x(t_i)\|^2+\|r_p(t_i)\|^2)
$$

</div>

<div class="math-panel">

$$
\mathcal L_{bdry}=\|x_\theta(0)-x^0\|^2+\|x_\theta(T)-x^T\|^2
$$

</div>
<p class="small">Total loss adds λ-weighted boundary matching and benchmark-specific velocity/obstacle terms.</p></div>
</div><div class="step-chain"><span>Boundary pair + collocation times</span><b>→</b><span>Penalized Hamiltonian H̄</span><b>→</b><span>Adam → L-BFGS</span></div><p class="protocol">No labeled trajectories · constraint barrier enters H̄ · finite residuals do not certify global optimality or continuous-time feasibility</p>
</div>

<!-- Explain the representation and training objective before showing speed claims. A fast forward map does not by itself establish generalization to arbitrary boundary conditions. -->

---
chapter: '7'
section: OCFormer · Baseline scaling
source: 'Thesis Chapter 7 · tab:oc:sympocnet; tab:oc:2d-scaling · 2D antipodal configurations'
---

# Scaling changes the cost of coordinated motion

<div class="density">
<div class="density-grid ">
<div class="detail-box"><h2>Matched baseline · 2D antipodal</h2><table><thead><tr><th>M</th><th>OCFormer J</th><th>SympOCNet J</th></tr></thead><tbody><tr><td>4</td><td>0.2003</td><td>0.2001</td></tr><tr><td>8</td><td>0.4036</td><td>0.4046</td></tr><tr><td>16</td><td>0.8307</td><td>0.8345</td></tr><tr><td>32</td><td>1.2531</td><td>1.4413</td></tr><tr><td>128</td><td>5.1424</td><td>infeasible</td></tr></tbody></table><p class="small">Same training budget in the baseline comparison; ≈13% lower cost at M = 32.</p></div>
<div class="detail-box"><h2>Source scaling protocol</h2><table><thead><tr><th>M</th><th>Gap to JLB</th><th>Min. clearance</th></tr></thead><tbody><tr><td>4</td><td>0.2%</td><td>1.3×10⁻⁴</td></tr><tr><td>8</td><td>0.9%</td><td>1.5×10⁻⁴</td></tr><tr><td>16</td><td>3.8%</td><td>1.5×10⁻⁴</td></tr><tr><td>32</td><td>8.4%</td><td>1.5×10⁻⁴</td></tr><tr><td>128</td><td>9.3%</td><td>1.2×10⁻⁴</td></tr></tbody></table><p class="small">Positive sampled margins up to 128 agents; lower cost alone does not establish feasibility.</p></div>
</div><p class="protocol">Per-instance optimization ≈20 min (regime-level timing, not per-row timings) · scaling margins evaluated on 5000 times · agent radius changes with M</p>
</div>

<!-- Values must match the source table. Cost gaps elsewhere are relative to a stated lower bound, not the unknown constrained optimum. -->

---
chapter: '7'
section: OCFormer · Inference regimes
source: 'Thesis Chapter 7 · tab:oc:regimes · Protocol-specific timing, not a single universal latency'
---

# Three regimes answer different deployment questions

<div class="density">
<table><thead><tr><th>Regime</th><th>Online work</th><th>Boundary coverage</th></tr></thead><tbody><tr><td>Per-instance</td><td>≈20 min optimization</td><td>One fixed pair</td></tr><tr><td>Transfer</td><td>Seconds of adaptation</td><td>Structured / small perturbations</td></tr><tr><td>Amortized</td><td>≈220 ms forward pass</td><td>Held-out in-distribution pairs</td></tr></tbody></table><div class="three"><div class="detail-box"><h2>Per-instance</h2><p class="small">New pair → initialize model → Adam/L-BFGS → trajectory</p><p class="small">Physics losses fit one latent curve.</p></div><div class="detail-box"><h2>Transfer</h2><p class="small">Trained model → changed pair → fine-tune → trajectory</p><p class="small">Freeze the trained backbone; adapt wrapper maps with L-BFGS.</p></div><div class="detail-box"><h2>Amortized</h2><p class="small">Many pairs offline → fixed model → new pair → trajectory</p><p class="small">No online weight updates within the tested distribution.</p></div></div><p class="protocol">Protocol-specific source timings · per-instance 3D examples do not inherit amortized 2D latency · transfer depends on perturbation size</p>
</div>

<!-- Timing is reproduced from the source protocol. The collection/export job times are unrelated to inference performance. -->

---
chapter: '7'
section: OCFormer · Amortized generalization
source: 'Thesis Chapter 7 · tab:oc:amortized · 100 rotated training pairs; JIT forward-pass timing over 100 runs'
---

# Fast inference does not guarantee feasibility

<div class="density">
<p class="protocol">Held-out rotations of 2D antipodal configurations · 100 rotated training pairs · JIT timing over 100 runs</p><table><thead><tr><th>M</th><th>Test cost</th><th>LB gap</th><th>Feasible</th><th>Inference</th></tr></thead><tbody><tr><td>8</td><td>0.4053</td><td>1.3%</td><td>100%</td><td>218.6 ± 1.3 ms</td></tr><tr><td>16</td><td>0.8399</td><td>5.0%</td><td>75%</td><td>220.9 ± 1.2 ms</td></tr></tbody></table><div class="density-grid ">
<div class="detail-box"><h2>Cost relative to free motion</h2>
<div class="math-panel">

$$
J_{LB}=\sum_i\frac{\|x_i^T-x_i^0\|^2}{2T},\quad \mathrm{gap}=\frac{J-J_{LB}}{J_{LB}}
$$

</div>
<p class="small">Lower bound omits collisions; the gap is not against the unknown constrained optimum.</p></div>
<div class="detail-box"><h2>Sampled feasibility</h2>
<div class="math-panel">

$$
c_{min}=\min_{i<j,t_k}(\|x_i(t_k)-x_j(t_k)\|-2r)
$$

</div>
<p class="small">Feasible fraction: held-out boundary pairs with positive minimum clearance. At M = 16, one quarter fails this test.</p></div>
</div><p class="protocol">Demonstrated: zero-shot rotated pairs · open: arbitrary boundaries, variable M, amortized 3D · timing ± source SD</p>
</div>

<!-- Feasibility is the fraction of held-out pairs with positive minimum inter-agent clearance. Keep the lower-bound denominator explicit. Full cost uncertainty is retained in the thesis table and backup provenance. -->

---
chapter: '7'
section: OCFormer · Two- and three-dimensional trajectories
source: 'Thesis Chapter 7 · 3D ball (16 agents) / 2D room (128 agents) · Saved per-instance L-BFGS trajectories; 200 frames each'
---

# Locate the encounter that determines clearance

<SwarmExamples />

<!-- Demo: play the motion, pause, rotate the view, then choose Closest pair. Read its time and margin together. The sphere is an agent-center exclusion zone of radius 0.1; agent radius is 0.02 for pairwise separation. Only sampled position constraints are checked, not continuous-time safety. -->
