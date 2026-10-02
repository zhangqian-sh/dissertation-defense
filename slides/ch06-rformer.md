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
source: 'Thesis Chapter 6 · fig:rformer:architecture; sec:rformer:attention'
---

# Separate what is observed from what is queried

<div class="cols wide-right" style="margin-top:16px"><div><div class="rule"><h2>Observation tokens</h2><p class="small">Position and measured value.</p></div><div class="rule" style="margin-top:25px"><h2>Query tokens</h2><p class="small">Position with zero-filled values; predictions are read at query locations.</p></div><p class="small" style="margin-top:24px">A structured attention mask encodes the token roles.</p></div><figure class="figure tall"><img src="/figures/ch06/rformer-architecture.png" alt="RFormer observation and query token architecture"><figcaption>Decoder-only transformer with a task-specific observation/query mask.</figcaption></figure></div>

<!-- Output at observation positions is discarded. Keep the source token roles and mask; do not substitute a generic causal language-model explanation. -->

---
chapter: '6'
section: RFormer · Mask and query chunking
source: 'Thesis Chapter 6 · sec:rformer:attention · Structured mask; source per-pass token budget'
---

# Bound memory while preserving the observation set

<div class="cols" style="margin-top:24px"><div class="rule"><h2>Information flow</h2><p class="small">Queries attend to all observations.</p><p class="small">Queries do not attend to other queries.</p><p class="small">Observations attend to preceding observations and themselves.</p></div><div class="rule"><h2>Large-field evaluation</h2><p class="small">Hold one observation subset fixed for the snapshot.</p><p class="small">Evaluate query chunks and restore original point order.</p><p class="small">Exclude padded entries from reconstructed output.</p></div></div>
<div class="takeaway">The source caps each sequence at 1024 tokens; memory follows the per-pass budget rather than the full point count.</div>

<!-- Chunking is a computational operation, not a new observation protocol. Query outputs do not depend on other unobserved queries under the mask. -->

---
chapter: '6'
section: RFormer · Vortex-street reconstruction
source: 'Thesis Chapter 6 · tab:rformer:vortex · Animation: saved RFormer case1/run-001 test outputs'
---

# Sparse observations recover coherent flow structure

<RFormerTime case-name="vortex" />
<p class="micro" style="margin-top:5px">Published total test relative RMSE: 0.0080 ± 0.0014 · mean ± source standard deviation.</p>

<!-- Play saved test snapshots in physical-time order. Rows are u, v, p; columns are reference, measured observations and RFormer. Observations are not interpolated. This is snapshot reconstruction, not autoregressive forecasting. -->

---
chapter: '6'
section: RFormer · Sparse and noisy data
source: 'Thesis Chapter 6 · fig:rformer:vortex-ablation · Error bars: one standard deviation across test snapshots'
---

# Observation density and noise are separate tests

<div class="cols" style="margin-top:15px"><figure class="figure"><img src="/figures/ch06/vortex-ablation-density.png" alt="Vortex reconstruction error versus observation density"><figcaption>Observation-density ablation</figcaption></figure><figure class="figure"><img src="/figures/ch06/vortex-ablation-noise.png" alt="Vortex reconstruction error versus measurement noise"><figcaption>Measurement-noise ablation</figcaption></figure></div>
<div class="takeaway">Robustness is conditional on the observation protocol. These curves do not establish a joint density–noise response surface.</div>

<!-- The source reports total relative RMSE below 0.016 for density 1–25%, and 0.094 at the highest tested noise. Preserve the original abscissa and uncertainty definitions. -->

---
chapter: '6'
section: RFormer · Turbulent-jet reconstruction
source: 'Thesis Chapter 6 · fig:rformer:jet-spectrum; tab:rformer:jet · Animation: saved jet outputs with paired validation truth'
---

# Compare both reconstructed fields and spectra

<div style="display:grid;grid-template-columns:2.3fr 1fr;gap:18px;align-items:center"><RFormerTime case-name="jet" /><figure class="figure"><img src="/figures/ch06/jet-baseline-spectrum.png" alt="Turbulent jet energy spectra across reconstruction baselines"><figcaption>Published baseline spectrum · static comparison, not the current frame.</figcaption></figure></div>
<div class="takeaway">Published total relative RMSE: 0.2540 ± 0.0131 · native 3D point cloud; displayed field is a projected slab.</div>

<!-- The uncertainty is the reported source standard deviation. This result does not establish a matched head-to-head comparison with ET. -->

---
chapter: '6'
section: RFormer · Continental weather reconstruction
source: 'Thesis Chapter 6 · Weather experiment · Saved case2/run-001 predictions; NOAA station TAVG (°C)'
---

# Reconstruct temperature across continental stations

<div style="display:grid;grid-template-columns:1fr 1.5fr;gap:22px;align-items:center"><figure class="figure"><img src="/figures/ch06/weather-stations.png" alt="Static weather station distribution"><figcaption>Static station distribution · 59 observations and 1961 query stations.</figcaption></figure><RecordedSequence name="weather" label="Weather date" caption="Reference / reconstructed · identically interpolated station fields · shared °C scale; not gridded ground truth." /></div>
<p class="micro">Weekly snapshots plus year-end. US land and station-coverage mask; missing station days were filled in source preprocessing.</p>

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
