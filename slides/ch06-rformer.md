---
chapter: '6'
section: Chapter 6 · Transition
source: 'Thesis Chapter 6 · Chapter overview'
divider: chapter
---

<div class="eyebrow">Chapter 6</div>
<div class="divider-rule" aria-hidden="true"></div>

# Reconstruction from Sparse Measurements: A Mesh-Free Approach with In-Context Learning

<!-- Spoken transition: How to do reconstruction which can scale?

Move from iterative energy dynamics to observation/query sequence modeling. Compare the reconstruction mechanisms without presenting one as a stage of the other. -->

---
chapter: '6'
section: RFormer · Representation
source: 'Thesis Chapter 6 · fig:rformer:architecture; sec:rformer:attention; eq:rformer:loss'
---

# Separate what is observed from what is queried

<div class="density">
<div class="density-grid ">
<figure class="figure"><img style="height:300px" src="/figures/ch06/rformer-architecture.png" alt="Interleaved observation/query tokens · query outputs decoded"><figcaption>Interleaved observation/query tokens · query outputs decoded</figcaption></figure>
<div class="detail-box"><h2>Tokenize coordinates and values</h2>
<div class="math-panel">

$$
O_i=[x_i,v_i],\qquad Q_j=[x_j,0]
$$

</div>
<p class="small">One linear embedding; coordinates carry position information. Query outputs define the reconstruction.</p>
<div class="math-panel">

$$
\mathcal L_Q=\frac{\sqrt{\sum_{j\in Q}\|\hat v_j-v_j\|_2^2}}{\sqrt{\sum_{j\in Q}\|v_j\|_2^2}}
$$

</div>
<p class="small">Observation outputs are discarded. Sample context/query sets during training; weights remain fixed during inference.</p></div>
</div><p class="protocol">4 layers · 8 heads · token width 128 · GELU · ≈350k parameters · Adam 10⁻³ · batch 16 · 100 epochs unless noted</p>
</div>

<!-- Output at observation positions is discarded. Keep the source token roles and mask; do not substitute a generic causal language-model explanation. -->

---
chapter: '6'
section: RFormer · Mask and query chunking
source: 'Thesis Chapter 6 · sec:rformer:attention · Structured mask; source per-pass token budget'
---

# Bound memory while preserving the observation set

<div class="density">
<div class="density-grid ">
<div class="detail-box"><h2>Allowed attention · grouped for display</h2><div class="attention-mask" role="img" aria-label="Grouped attention diagram: observations attend to preceding observations and themselves; queries attend to observations; all query-key connections are blocked"><span></span><b>Keys: O</b><b>Keys: Q</b><b>Rows: O</b><span class="allowed">Lower triangular<br>preceding O + self</span><span class="blocked">Blocked</span><b>Rows: Q</b><span class="allowed">All observations</span><span class="blocked">Blocked</span></div><p class="small">O = observations; Q = queries. Actual input remains interleaved; grouping only explains the mask.</p>
<div class="math-panel">

$$
A=\operatorname{softmax}(QK^\top/\sqrt{d}+M)
$$

</div>
<p class="small">d = head width; M = 0 on allowed connections, −∞ on blocked connections.</p></div>
<div class="detail-box"><h2>Chunk evaluation · fixed context</h2><ol class="algorithm"><li>Draw one observation subset O for this snapshot.</li><li>Partition target coordinates into query chunks Q₁,…,Qᵣ.</li><li>Evaluate each [O,Qᵣ] sequence with the same context.</li><li>Remove padded outputs; restore original point order.</li></ol><p class="small">No query-to-query attention: adding other unknown targets does not supply new information.</p></div>
</div><p class="protocol">≤1024 tokens per pass, including observations · attention memory follows the per-pass token budget · more queries require more passes</p>
</div>

<!-- Chunking is a computational operation, not a new observation protocol. Query outputs do not depend on other unobserved queries under the mask. -->

---
chapter: '6'
section: RFormer · Vortex-street reconstruction
source: 'Thesis Chapter 6 · tab:rformer:vortex · Animation: saved RFormer case1/run-001 test outputs'
---

# Sparse observations recover coherent flow structure

<RFormerTime case-name="vortex" />
<p class="micro" style="margin-top:5px">Snapshot reconstruction · 512 observations · total test relative RMSE 0.0080 ± 0.0014 (source SD); no autoregressive forecasting.</p>

<!-- Play saved test snapshots in physical-time order. Rows are u, v, p; columns are reference, measured observations and RFormer. Observations are not interpolated. This is snapshot reconstruction, not autoregressive forecasting. -->

---
chapter: '6'
section: RFormer · Sparse and noisy data
source: 'Thesis Chapter 6 · fig:rformer:vortex-ablation · Error bars: one standard deviation across test snapshots'
---

# Observation density and noise are separate tests

<div class="density">
<div class="density-grid ">
<figure class="figure"><img style="height:275px" src="/figures/ch06/vortex-ablation-density.png" alt="Observation-density sweep · 1–25%"><figcaption>Observation-density sweep · 1–25%</figcaption></figure>
<figure class="figure"><img style="height:275px" src="/figures/ch06/vortex-ablation-noise.png" alt="Separate measurement-noise sweep"><figcaption>Separate measurement-noise sweep</figcaption></figure>
</div><div class="density-grid ">
<div class="detail-box"><h2>Sparsity</h2><p class="small">Reported total relative RMSE stays below 0.016 over the tested density range.</p></div>
<div class="detail-box"><h2>Noise</h2><p class="small">Reported total relative RMSE reaches 0.094 at the highest tested noise.</p></div>
</div><p class="protocol">Error bars: one SD across test snapshots · retain original noise axis · separate sweeps do not establish joint density–noise robustness</p>
</div>

<!-- The source reports total relative RMSE below 0.016 for density 1–25%, and 0.094 at the highest tested noise. Preserve the original abscissa and uncertainty definitions. -->

---
chapter: '6'
section: RFormer · Turbulent-jet reconstruction
source: 'Thesis Chapter 6 · fig:rformer:jet-spectrum; tab:rformer:jet · Animation: saved jet outputs with paired validation truth'
---

# Compare both reconstructed fields and spectra

<div style="display:grid;grid-template-columns:2.3fr 1fr;gap:18px;align-items:center"><RFormerTime case-name="jet" /><figure class="figure"><img src="/figures/ch06/jet-baseline-spectrum.png" alt="Turbulent jet energy spectra across reconstruction baselines"><figcaption>Published baseline spectrum · static comparison, not the current frame.</figcaption></figure></div>
<div class="takeaway">1000 observations (≈10%) · 160 training / 40 test snapshots · total relative RMSE 0.2540 ± 0.0131 (source SD) · projected 3D slab.</div>

<!-- The uncertainty is the reported source standard deviation. This result does not establish a matched head-to-head comparison with ET. -->

---
chapter: '6'
section: RFormer · Continental weather reconstruction
source: 'Thesis Chapter 6 · Weather experiment · Saved case2/run-001 predictions; NOAA station TAVG (°C)'
---

# Reconstruct temperature across continental stations

<div style="display:grid;grid-template-columns:1fr 1.5fr;gap:22px;align-items:center"><figure class="figure"><img src="/figures/ch06/weather-stations.png" alt="Static weather station distribution"><figcaption>Static station distribution · 59 observations and 1961 query stations.</figcaption></figure><RecordedSequence name="weather" label="Weather date" caption="Reference / reconstructed · identically interpolated station fields · shared °C scale; not gridded ground truth." /></div>
<p class="micro">54 recorded dates in 2024 · weekly plus year-end · 59 measured / 1961 query stations · TAVG (°C). US land/coverage mask; source-filled missing days.</p>

<!-- Play through the recorded seasons. Smoothing is spatial only and does not turn station predictions into a numerical ground-truth field. -->

---
chapter: '6'
section: RFormer · Blood-flow reconstruction
source: 'RFormer manuscript · blood_snapshot_u / blood_snapshot_v · Original published 2×2 snapshot comparisons'
---

# Compare blood-flow observations and reconstruction

<div class="cols" style="margin-top:18px"><figure class="figure"><img src="/figures/ch06/blood-snapshot-u.png" alt="Blood u velocity: sparse observations, raw/full target, RFormer reconstruction, averaged-grid reference"><figcaption>u velocity · original 2×2 snapshot</figcaption></figure><figure class="figure"><img src="/figures/ch06/blood-snapshot-v.png" alt="Blood v velocity: sparse observations, raw/full target, RFormer reconstruction, averaged-grid reference"><figcaption>v velocity · original 2×2 snapshot</figcaption></figure></div>
<p class="micro">Raw/full targets and averaged-grid references are distinct. Published total relative RMSE: RFormer 0.6604 ± 0.0267; TNP 0.6616 ± 0.0267; CNP 0.6630 ± 0.0260—nearly tied.</p>

<!-- Static published snapshots replace playback. Preserve each panel’s distinction between raw/full targets and averaged-grid references; do not interpret them as interchangeable ground truths. -->
