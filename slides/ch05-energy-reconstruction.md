---
chapter: '5'
section: Energy Transformer · Reconstruction
source: 'Thesis Chapter 5 · fig:et:workflow · Reconstruction from sparse observations'
---

# Infer a complete field from partial observations

<div class="cols wide-right" style="margin-top:20px"><div><div class="eyebrow">Part II · Sequence-to-sequence modeling</div><h2>Energy Transformer</h2><p class="small">Represent a field as patch tokens and reconstruct missing information through learned energy dynamics.</p><p class="small">The inference state evolves; the trained weights remain fixed.</p></div><figure class="figure tall"><img src="/figures/ch05/et-workflow.png" alt="Energy Transformer sparse observation reconstruction workflow"><figcaption>Patch tokenization, energy-based inference and field reconstruction.</figcaption></figure></div>

<!-- This begins the independent reconstruction part. There is no demonstrated SNN-to-reconstruction-to-control pipeline. -->

---
chapter: '5'
section: Energy Transformer · Token dynamics
source: 'Thesis Chapter 5 · fig:et:architecture; eq:et:update · Niter=12, step size 0.1'
---

# At inference, tokens move through a learned energy

<div class="cols" style="margin-top:20px"><figure class="figure"><img src="/figures/ch05/et-block.png" alt="Energy Transformer block with attention and Hopfield terms"><figcaption>Energy attention couples tokens; the Hopfield term acts within tokens.</figcaption></figure><figure class="figure"><img src="/figures/ch05/et-energy-update.png" alt="Source energy minimization update schematic"><figcaption>Source update schematic. Its t denotes an inference iteration.</figcaption></figure></div>
<div class="takeaway">Initialize tokens → normalize → evaluate energy → update tokens → detokenize. The source benchmarks use 12 inference iterations.</div>

<!-- This diagram explains the update. The following slide replays the saved masked input through the saved checkpoint. Do not imply monotonic energy decrease or clamped observed tokens. -->

---
chapter: '5'
section: Energy Transformer · Reconstruction history
source: 'ETRO 2D vortex street · test sample 0 · 90% nominal masking · α=0.1 · Replay/archived output ΔL₂=0.111%'
---

# Follow reconstruction through the token updates

<EnergyHistory />

<!-- Demo: compare saved masked input and reference, then play updates 1–12 or scroll over the fields. This is the 2D vortex-street v component at native 128×256 resolution, shown without display smoothing. Energy covers all tokens; error covers v. Replay differs from archived output by 0.111% relative L2, with unresolved cause; history endpoint agrees with ordinary inference in the replay runtime. -->

---
chapter: '5'
section: Energy Transformer · Field reconstruction
source: 'Thesis Chapter 5 · fig:et:3djet-results · Native published cross-sections'
---

# Reconstruct spatial structure in a turbulent jet

<figure class="figure" style="margin-top:12px"><img style="height:165px" src="/figures/ch05/et-3djet-results-u.png" alt="Turbulent jet streamwise velocity reconstruction and reference"><figcaption>Streamwise velocity: published reference and reconstruction panels.</figcaption></figure>
<figure class="figure" style="margin-top:14px"><img style="height:165px" src="/figures/ch05/et-3djet-results-v.png" alt="Turbulent jet cross stream velocity reconstruction and reference"><figcaption>Cross-stream velocity: spatial structure under the source observation protocol.</figcaption></figure>

<!-- These are fixed source slices, not a reconstruction of arbitrary 3D values from images. Discuss the correspondence of coherent structures before turning to quantitative fidelity. -->

---
chapter: '5'
section: Energy Transformer · Pointwise fidelity
source: 'Thesis Chapter 5 · fig:et:pinn-rel-err; sec:et:fidelity · Source 3D turbulent-jet test interval'
---

# Pointwise error is one part of physical fidelity

<div class="cols" style="margin-top:15px"><figure class="figure"><img src="/figures/ch05/et-pinn-rel-err.png" alt="PINN relative errors through the test interval"><figcaption>PINN baseline</figcaption></figure><figure class="figure"><img src="/figures/ch05/et-rel-err.png" alt="Energy Transformer relative errors through the test interval"><figcaption>Energy Transformer</figcaption></figure></div>
<div class="takeaway">PINN can have lower pointwise velocity error. A second diagnostic is needed to assess fine-scale structure.</div>

<!-- Keep this limitation explicit. The next slide supplies kinetic-energy spectra, not a claim that ET dominates all metrics. -->

---
chapter: '5'
section: Energy Transformer · Spectral fidelity
source: 'Thesis Chapter 5 · fig:et:pinn-spectrum · Kinetic-energy spectra on the turbulent-jet benchmark'
---

# Spectra reveal fine scales that errors can miss

<div class="cols" style="margin-top:15px"><figure class="figure"><img src="/figures/ch05/et-pinn-spectrum.png" alt="PINN kinetic energy spectrum compared with reference"><figcaption>PINN: high-wavenumber content is attenuated.</figcaption></figure><figure class="figure"><img src="/figures/ch05/et-spectrum.png" alt="Energy Transformer kinetic energy spectrum compared with reference"><figcaption>ET: improved retention of high-wavenumber energy.</figcaption></figure></div>
<div class="takeaway">Evaluate pointwise agreement and spectral structure together.</div>

<!-- Pair the conclusion with the preceding error plots. Do not translate spectral fidelity into uniformly lower pointwise error. -->

---
chapter: '5'
section: Energy Transformer · Inference cost
source: 'Thesis Chapter 5 · tab:et:timing · Single NVIDIA A6000; 12 inference iterations'
---

# Separate offline training from iterative inference

<table style="margin-top:25px"><thead><tr><th>Benchmark</th><th>Total training</th><th>Inference per snapshot</th></tr></thead><tbody><tr><td>2D vortex street</td><td>≈ 90 min</td><td>≈ 2.7 ms</td></tr><tr><td>2D Schlieren jet</td><td>≈ 150 min</td><td>≈ 2.5 ms</td></tr><tr><td>3D turbulent jet</td><td>≈ 70 min</td><td>≈ 100 ms</td></tr></tbody></table>
<div class="cols" style="margin-top:28px"><div class="rule"><h2>Repeated reconstruction</h2><p class="small">The trained energy is reused across snapshots.</p></div><div class="rule teal"><h2>A bounded operating regime</h2><p class="small">Distribution shift and observation changes can alter reconstruction quality.</p></div></div>

<!-- Times are source measurements with the stated hardware and iteration count. These are not performance measurements of the presentation or a matched comparison with RFormer. -->
