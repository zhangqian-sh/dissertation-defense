---
chapter: '6'
section: Part II · Sequence-to-sequence modeling
source: 'Thesis Chapter 6 · Chapter overview'
divider: chapter
---

<p class="divider-chapter">Chapter 6</p>
<div class="divider-rule" aria-hidden="true"></div>

# Reconstruction from Sparse Measurements: A Mesh-Free Approach with In-Context Learning

<!-- Spoken transition: How to do reconstruction which can scale?

Move from iterative energy dynamics to observation/query sequence modeling. Compare the reconstruction mechanisms without presenting one as a stage of the other. -->

---
chapter: '6'
section: RFormer · Representation
source: 'Thesis Chapter 6 · fig:rformer:architecture; sec:rformer:attention;
  eq:rformer:loss'
---

# RFormer: Meshfree Reconstruction

<div class="et-reconstruction-layout rformer-reconstruction-layout">
<section class="et-reconstruction-description">
<h2>Reconstruction operator</h2>
<p>A map from the <strong>space of sparsely observed functions</strong> to the <strong>space of fully reconstructed functions</strong>.</p>

$$
\mathcal R:\;v|_{\Omega_{\mathcal O}}\longmapsto\widehat v,
\qquad \widehat v:\Omega\to\mathbb R^{d_v}
$$

<p>Represent the observed function by position–value pairs. Query its reconstruction at any unobserved position:</p>

$$
\mathcal P_{\mathcal O}=\{(x_i,v_i)\}_{i\in\mathcal O},
\qquad \widehat v(x)=\mathcal R_\theta(x;\mathcal P_{\mathcal O})
$$

<h2 class="et-reconstruction-subheading">RFormer realizes this map</h2>
<p>RFormer treats reconstruction as <strong>in-context question answering</strong> on an unstructured point set.</p>
<ul>
<li><strong>Context:</strong> embed observed position–value pairs <InlineMath tex="[x_i,v_i]" />.</li>
<li><strong>Query:</strong> embed target positions with unknown values <InlineMath tex="[x_j,\mathbf 0]" />.</li>
<li><strong>Answer:</strong> use masked attention to gather observed information; decode values at query positions.</li>
</ul>
<p class="rformer-learning-note">Train on sampled observation/query sets. At inference, change the context and queries while keeping the learned weights fixed.</p>
</section>
<section class="rformer-reconstruction-example">
<figure class="figure rformer-architecture">
<img src="/figures/ch06/rformer-architecture.png" alt="Decoder-only transformer with interleaved observed position–value tokens and query-position tokens; query outputs provide reconstructed values">
<figcaption>Observations + query positions → reconstructed values</figcaption>
</figure>
<div class="rformer-weather-example">
<div class="rformer-weather-heading"><h2>Illustration</h2><div class="rformer-weather-key"><span><i class="rformer-position-key"></i><InlineMath tex="x" />: city</span><span><i class="rformer-value-key"></i><InlineMath tex="v" />: temperature</span></div></div>
<div class="rformer-weather-sequence">
<div class="rformer-weather-group"><strong>Context</strong><div class="rformer-weather-context"><span class="rformer-weather-pair"><span class="rformer-weather-position">New York</span><span class="rformer-weather-value">20</span></span><span class="rformer-weather-pair"><span class="rformer-weather-position">Boston</span><span class="rformer-weather-value">17</span></span></div></div>
<span class="rformer-weather-arrow" aria-hidden="true">→</span>
<div class="rformer-weather-group"><strong>Query</strong><span class="rformer-weather-position">Providence</span></div>
<span class="rformer-weather-arrow" aria-hidden="true">→</span>
<div class="rformer-weather-group"><strong>Answer</strong><span class="rformer-weather-value">18</span></div>
</div>
</div>
</section>
</div>

<!--
Weather example uses illustrative temperatures (20, 17, 18), not measured predictions, to demonstrate the paper's context/query/answer formulation. Coordinates are physical positions; zero is the query's unknown-value placeholder. The learned operator conditions on measurements from the same snapshot, rather than forecasting the next time step. Outputs at observation positions are discarded.
-->

---
chapter: '6'
section: RFormer · Continental weather reconstruction
source: 'Thesis Chapter 6 · Weather experiment · Saved case2/run-001
  predictions; NOAA station TAVG (°C)'
---

# Example: US Weather
<div class="rformer-weather-layout">
<section class="rformer-weather-left">
<div class="rformer-weather-setup">
<h2>Setup</h2>
<p>Reconstruct the <strong>daily mean temperature</strong> (°C) at unobserved NOAA stations across the contiguous United States.</p>

$$
\widehat T(x)=\mathcal R_\theta\!\left(x;\{(x_i,T_i)\}_{i\in\mathcal O}\right)
$$

<p><strong>Observations:</strong> 59 stations provide context; the remaining 1961 stations are queries. Each position <InlineMath tex="x" /> contains latitude and longitude.</p>
<p><strong>Training:</strong> 2020–2023. <strong>Testing:</strong> all 366 daily snapshots of 2024.</p>
</div>
<figure class="figure rformer-station-distribution"><img src="/figures/ch06/weather-stations.png" alt="Distribution of 2020 NOAA stations across the contiguous United States, with 59 selected observation stations in orange"><figcaption>Station distribution · orange: observations; blue: all stations</figcaption></figure>
</section>
<RecordedSequence name="weather" label="Weather date" caption="" />
</div>
<!-- Display every other day of 2024 (183 snapshots); evaluation retains all 366 daily snapshots. Fixed temperature color range [-30, 40] °C. Display fields interpolate station data spatially; source preprocessing fills missing station days. -->

<!--
Play through the recorded seasons. Smoothing is spatial only and does not turn station predictions into a numerical ground-truth field.
-->

---
chapter: '6'
section: RFormer · Vortex-street reconstruction
source: 'Thesis Chapter 6 · tab:rformer:vortex; fig:rformer:vortex-ablation ·
  Animation: saved RFormer case1/run-001 test outputs'
---

# Example: 2d Vortex Street
<div class="rformer-vortex-layout">
<section class="rformer-vortex-reconstruction">
<RFormerTime case-name="vortex" compact />
<p class="rformer-vortex-metric">512 / 29,180 measured points (1.75%) · test relative RMSE: 0.0080 ± 0.0014.</p>
</section>
<section class="rformer-vortex-ablation">
<figure class="figure"><img src="/figures/ch06/vortex-ablation-density.png" alt="Vortex reconstruction error versus observation density from 1 to 25 percent"><figcaption>Observation density</figcaption><p>Total relative RMSE &lt; 0.016.</p></figure>
<figure class="figure"><img src="/figures/ch06/vortex-ablation-noise.png" alt="Vortex reconstruction error versus measurement noise in a separate sweep"><figcaption>Measurement noise</figcaption><p><InlineMath tex="\delta_c\sim\mathcal N(0,(\nu\sigma_c)^2)" /> added to observations.</p></figure>
<p class="rformer-vortex-ablation-note"><InlineMath tex="\sigma_c" />: training-data SD of each component. Error bars: ±1 SD; separate sweeps.</p>
</section>
</div>

<!--
Saved test snapshots are played in physical-time order; rows u/v/p and columns reference/observed/reconstructed retain fixed row scales. This is snapshot reconstruction, not autoregressive forecasting. Published ablation figures retain their original axes and error bars. Density and noise are separate experiments. Former ch6-28 is merged into this slide.
-->

---
chapter: '6'
section: RFormer · Blood-flow reconstruction
source: 'RFormer val.h5 · linear interpolation and reconstruction on averaged-grid reference; 20 matched snapshots'
---

# Example: Blood Flow
<BloodSnapshotGrid />

<!--
Eight panels loop through raw snapshots 0–19 and matched averaged-grid snapshots 80–99 using the original analysis_publication.ipynb alignment, midplane |z|<1. Static/print fallback uses snapshots 5/85. Rows u/v; columns observations, linear interpolation, reconstruction, averaged-grid reference. Shared robust 99th-percentile symmetric color limits within each component; no color bars. Native labels use Noto Serif and default KaTeX, with 12px axes. Interpolation and RFormer are recomputed on the same averaged grid using 3D linear interpolation with nearest fill. Metrics use full 3D velocity vectors and a shared finite reference mask within [-10,10], without clipping, averaged over 20 snapshots. This validity range follows the original notebook; excluded reference counts are recorded in the blood animation index.
-->

---
chapter: '6'
section: RFormer · Turbulent-jet reconstruction
source: 'Thesis Chapter 6 · fig:rformer:jet-spectrum; tab:rformer:jet ·
  Animation: saved jet outputs with paired validation truth'
---

# Example: 3d Turbulent Jet Flow

<div style="display:grid;grid-template-columns:2.3fr 1fr;gap:18px;align-items:center"><RFormerTime case-name="jet" /><figure class="figure"><img src="/figures/ch06/jet-baseline-spectrum.png" alt="Turbulent jet energy spectra across reconstruction baselines"></figure></div>

<div class="rformer-jet-explanation">
<section>
<h3>Experimental setup</h3>
<p>Particle tracking velocimetry measures the velocity of the turbulent jet. RFormer reconstructs the unobserved velocities from 10% of the measured points, using 80% snapshots for training and 20% for testing. The animation shows in-plane velocity vectors in the <InlineMath tex="|z|<5" /> slab.</p>
</section>
<section>
<h3>Energy spectryn</h3>
<p>The energy spectrum <InlineMath tex="E(k)" /> describes how kinetic energy is distributed across spatial scales: low wavenumbers represent large structures, high wavenumbers small structures. RFormer closely follows the reference peak and spectral decay, while most baselines lose energy at smaller scales. The dashed <InlineMath tex="k^{-5/3}" /> line is a reference for inertial-range scaling.</p>
</section>
</div>

<!--
The uncertainty is the reported source standard deviation. This result does not establish a matched head-to-head comparison with ET.
-->
