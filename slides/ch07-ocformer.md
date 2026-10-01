---
chapter: '7'
section: OCFormer · Optimal-control formulation
source: 'Thesis Chapter 7 · Problem formulation and Hamiltonian system'
---

# Coordinated motion under coupled constraints

$$
\min_{\mathbf x,\mathbf u}\int_0^T L(\mathbf x(t),\mathbf u(t))\,dt
\quad\text{subject to dynamics, boundaries, and }h(\mathbf x)\geq0
$$

<div class="three" style="margin-top:35px"><div class="rule"><h2>Boundary conditions</h2><p class="small">Move from prescribed initial positions to prescribed terminal positions.</p></div><div class="rule"><h2>Agent interactions</h2><p class="small">Maintain pairwise clearance across a coordinated trajectory.</p></div><div class="rule"><h2>Environmental constraints</h2><p class="small">Avoid the geometry defined by each benchmark.</p></div></div>
<div class="takeaway">Trajectory cost and feasibility are separate outcomes; low cost alone is insufficient.</div>

<!-- This is a separate optimal-control study. Do not imply its input fields came from the reconstruction models. -->

---
chapter: '7'
section: OCFormer · Latent and physical coordinates
source: 'Thesis Chapter 7 · fig:oc:latent-physical; fig:oc:architecture · State–costate transformation'
---

# Learn a map from latent to physical trajectories

<div class="cols" style="margin-top:15px"><RecordedSequence name="latent" label="Latent and optimized trajectory time" caption="Left: straight endpoint reference. Right: saved L-BFGS optimized trajectories from the paper’s run; not a hand-designed detour." /><figure class="figure"><img src="/figures/ch07/ocformer-architecture.png" alt="OCFormer attention based transformation architecture"><figcaption>Attention-based architecture for interacting agents.</figcaption></figure></div>
<div class="takeaway">Physics-informed training constrains the learned map. A trajectory overlay is not proof of a diffeomorphism.</div>

<!-- OCFormer is permutation-equivariant, not asserted symplectic. The latent-map motivation includes a diffeomorphism assumption; preserve that distinction. -->

---
chapter: '7'
section: OCFormer · Physics-informed training
source: 'Thesis Chapter 7 · fig:oc:training · Hamiltonian residuals and boundary matching'
---

# Train the trajectory map with physics and boundaries

<div class="cols wide-right" style="margin-top:20px"><div><h2>A learned solution representation</h2><p class="small">Evaluate the state–costate map along latent trajectories.</p><p class="small">Differentiate through the map to form Hamiltonian residuals.</p><p class="small">Combine residual, boundary, and problem-specific constraint penalties.</p></div><figure class="figure tall"><img src="/figures/ch07/training-flowchart.png" alt="OCFormer physics informed training flowchart"><figcaption>Source training diagram. Per-instance optimization and amortized evaluation use different protocols.</figcaption></figure></div>

<!-- Explain the representation and training objective before showing speed claims. A fast forward map does not by itself establish generalization to arbitrary boundary conditions. -->

---
chapter: '7'
section: OCFormer · Baseline scaling
source: 'Thesis Chapter 7 · tab:oc:sympocnet; tab:oc:2d-scaling · 2D antipodal configurations'
---

# Scaling changes the cost of coordinated motion

<div class="cols" style="margin-top:24px"><table><thead><tr><th>Agents</th><th>OCFormer cost</th><th>SympOCNet cost</th></tr></thead><tbody><tr><td>4</td><td>0.2003</td><td>0.2001</td></tr><tr><td>8</td><td>0.4036</td><td>0.4046</td></tr><tr><td>16</td><td>0.8307</td><td>0.8345</td></tr><tr class="highlight"><td>32</td><td>1.2531</td><td>1.4413</td></tr><tr><td>128</td><td>5.1424</td><td>— · infeasible</td></tr></tbody></table><div class="rule"><h2>Read cost with feasibility</h2><p class="small">Near-parity at smaller agent counts.</p><p class="small">The source reports a lower cost at M=32 and failed convergence for the SympOCNet M=128 case.</p><p class="small">These are 2D per-instance results, separate from the upcoming 3D scene.</p></div></div>

<!-- Values must match the source table. Cost gaps elsewhere are relative to a stated lower bound, not the unknown constrained optimum. -->

---
chapter: '7'
section: OCFormer · Inference regimes
source: 'Thesis Chapter 7 · tab:oc:regimes · Protocol-specific timing, not a single universal latency'
---

# Three regimes answer different deployment questions

<table style="margin-top:25px"><thead><tr><th>Regime</th><th>Work per new problem</th><th>Scope</th></tr></thead><tbody><tr><td>Per-instance</td><td>≈ 20 min optimization</td><td>One fixed boundary pair</td></tr><tr><td>Transfer</td><td>Seconds of adaptation</td><td>Structured or small perturbations</td></tr><tr class="highlight"><td>Amortized</td><td>≈ 220 ms forward pass</td><td>Held-out, in-distribution pairs</td></tr></tbody></table>
<div class="takeaway">The online speedup changes what must be learned offline and what boundary variation is covered.</div>
<p class="small" style="margin-top:24px">A per-instance 3D trajectory does not inherit the amortized 2D latency claim.</p>

<!-- Timing is reproduced from the source protocol. The collection/export job times are unrelated to inference performance. -->

---
chapter: '7'
section: OCFormer · Amortized generalization
source: 'Thesis Chapter 7 · tab:oc:amortized · 100 rotated training pairs; JIT forward-pass timing over 100 runs'
---

# Fast inference does not guarantee feasibility

<p class="subtitle">Held-out rotations of 2D antipodal configurations.</p>
<table><thead><tr><th>Agents</th><th>Test cost</th><th>Gap vs. lower bound</th><th>Feasibility</th><th>Inference</th></tr></thead><tbody><tr><td>8</td><td>0.4053</td><td>1.3%</td><td>100%</td><td>218.6 ± 1.3 ms</td></tr><tr class="highlight"><td>16</td><td>0.8399</td><td>5.0%</td><td>75%</td><td>220.9 ± 1.2 ms</td></tr></tbody></table>
<div class="cols" style="margin-top:27px"><div class="rule"><h2>What is demonstrated</h2><p class="small">Zero-shot inference within the trained rotation distribution.</p></div><div class="rule"><h2>What remains open</h2><p class="small">Arbitrary boundaries, variable agent counts, and amortized 3D room navigation.</p></div></div>

<!-- Feasibility is the fraction of held-out pairs with positive minimum inter-agent clearance. Keep the lower-bound denominator explicit. Full cost uncertainty is retained in the thesis table and backup provenance. -->

---
chapter: '7'
section: OCFormer · Two- and three-dimensional trajectories
source: 'Thesis Chapter 7 · 3D ball (16 agents) / 2D room (128 agents) · Saved per-instance L-BFGS trajectories; 200 frames each'
---

# Locate the encounter that determines clearance

<SwarmExamples />

<!-- Demo: play the motion, pause, rotate the view, then choose Closest pair. Read its time and margin together. The sphere is an agent-center exclusion zone of radius 0.1; agent radius is 0.02 for pairwise separation. Only sampled position constraints are checked, not continuous-time safety. -->
