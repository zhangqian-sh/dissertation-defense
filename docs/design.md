# Thesis defense presentation design

The deck is mostly publication-quality static slides, with purposeful dynamic figures where time or three-dimensional structure cannot be shown clearly in a few panels. This replaces the earlier Tier 1–3 widget-per-topic design. See [file_structure.md](file_structure.md) for sources/layout and [plan.md](plan.md) for implementation.

## 1. Narrative and interaction criteria

The presentation theme follows [Brown's official Visual Identity color guide](https://policy.brown.edu/sites/default/files/policy/related/Brown_Visual_Identity_Policy_2016-07-22.pdf), printed pages 19–20. Main colors are brown `#4E3629` for headings, small text, and all horizontal bars above text sections and workflow steps; full-tint red `#ED1C24` marks takeaways, progress indicators, and title accents. Horizontal bars group content without assigning different importance to comparison columns. The primary accent tokens are gold `#FFC72C` and gray `#98A4AE`. White backgrounds and subtle screens of brown keep the deck readable; published figures, scientific field scales, and comparison-series colors retain their source meanings. Theme colors are centralized in `style.css`.

Slides must follow the thesis order: **1 Introduction → 2 Spiking representations and SMS → 3 Conversion and Loihi 2 → 4 RFG → 5 Energy Transformer → 6 RFormer → 7 OCFormer → 8 Summary.** Implementation scheduling does not change slide order.

Preserve the two independent themes: Part I neuromorphic algorithms and Part II sequence-to-sequence studies of reconstruction and optimal control. No experimentally demonstrated reconstruction-to-control pipeline is claimed.

Use interaction when it reveals information that readable static panels cannot reasonably show: a long sequence, spatial occlusion, or a critical event linked to quantitative evidence. A selector between a few methods/settings is not sufficient justification. Show comparisons simultaneously so the audience does not have to remember a previous image.

Distinguish ordinary slide reveals, scripted animation, and interactive inspection. Rehearse an animation sequence for the talk; expose pause, scrubbing, and viewpoint controls for explanation and questions. The argument must not depend on spontaneous dashboard exploration.

| Treatment | Content |
|---|---|
| Required interaction | SMS/SDON rollout and T approximation; conversion output over T; OCFormer trajectory inspection |
| Conditional interaction | ET iteration playback; RFormer volume/slice inspection, only after reviewing the evidence |
| Static main slides | Encoding, calibration, hardware scaling, RFG comparisons, ET physical fidelity, RFormer architecture/results, OCFormer regimes/baselines |
| Static backups | Extra rollout/swarm cases, ET module/temporal ablations, detailed dataset comparisons |
| Outside current scope | Attention-weight inspector, continuous latent/physical morph, generic method/dataset dashboards, clickable claim map |

A conditional interaction is not an unfinished requirement. A documented decision to use static panels fully satisfies that topic.

## 2. Chapter-ordered presentation map

| Chapter | Scientific content | Treatment |
|---|---|---|
| 1 | Questions, contributions, two-theme organization | Static thesis map with staged highlights; reuse at closing |
| 2 | Encoding and Poisson operator accuracy | Aligned rasters, same-sample solution panels, held-out error statistics |
| 2 | SMS one-step versus cascade behavior | Required playback/scrubbing and aligned error traces |
| 3 | Calibration method and accuracy | Layerwise schematic, theorem interpretation, ANN/uncalibrated/calibrated panels, compact horizon comparison |
| 3 | Converted SNN output over T | Required recording of output evolution across the loop |
| 3 | Loihi precision and resource trade-off | Both precisions on throughput/energy/EDP curves versus replicas; annotate chip transition |
| 4 | Forward JVP training and accuracy cost | Staged global/layerwise schematic plus BP/RFG predictions and error distributions |
| 5 | Patch tokens, learned energy, token updates | Static workflow and representative iteration frames; conditional playback |
| 5 | Physical fidelity and inference cost | ET/PINN fields, errors, and spectra together; separate training from iterative inference timing |
| 6 | Context/query roles, attention mask, chunking | Staged architectural schematic; no attention-weight export |
| 6 | Sparse/noisy reconstruction and baselines | Vortex small multiples and separate density/noise curves; jet field/spectrum comparison; qualified weather/blood examples |
| 6 | Geometry hidden by a fixed view | Conditional synchronized rotation/slicing; otherwise fixed slices or native-coordinate plots |
| 7 | Latent solution, state–costate map, physics-informed training | Static latent/physical overlay, architecture and loss schematic |
| 7 | Moving agents and constraint events | Required playback, scrubbing, 3D camera, closest-encounter inspection |
| 7 | Baseline scaling and inference regimes | Static OCFormer/SympOCNet comparison; timing/cost/feasibility together |
| 8 | Demonstrated contributions and limitations | Static synthesis reusing prior evidence |

RFG experimental results, ET spectral fidelity, Loihi replication scaling, RFormer tokenization, and OCFormer feasibility are core content even though they do not require widgets.

## 3. Interaction specifications

Each checkbox in this section represents one interactive plot. The unmarked bullets below each plot record its scope and implementation details.

### Chapter 2 — SMSRollout (required)

Primary question: how does recursive prediction evolve and accumulate error beyond the training interval?

- [x] (required) SMSRollout / SDON-SMS: interactively show the reference, one-step and recursive cascade predictions, their error evolution, and the stepwise approximation to the continuous value as T changes.

Plot details:

- Select one documented ODE/PDE case for clarity; no required scenario menu.
- Play/pause advances a common physical-time index. Scrubbing moves markers on reference, prediction (non-cascade and cascade), and error views together.
- Permanently mark the training/extrapolation boundary. Keep physical time distinct from internal spike horizon K.
- Choose T values to show how the stepwise function approximates the continuous value.
- Reset returns to the rehearsed start. The static fallback shows representative times and full error traces.
- Firing histories, decoded bounds, and a documented ANN comparator are optional supporting evidence, not mandatory payload decorations.

Bounded decoded values are a property of the codec, not a general stability/convergence theorem. Do not invent a PINN blow-up comparison.

### Chapter 3 — Conversion over T (required)

Primary question: how does the converted SNN output evolve as the SNN loops over T?

- [x] (required) Conversion: interactively record and show the converted SNN output at each loop step through T.

### Chapter 7 — DroneSwarm3D (required)

Primary question: when and where do paths negotiate obstacles/collisions, and which encounter determines measured clearance?

- [x] (required) DroneSwarm3D: interactively inspect synchronized agent trajectories, clearance traces, depth separation, and closest-encounter events.

Plot details:

- Play/pause and time scrubbing move agents and a clearance-trace cursor in synchrony.
- Orbit/pan/zoom reveals depth separation; include camera reset. Use a planar camera for 2D cases.
- “Closest encounter” jumps to an exported critical time, highlights the pair or agent/obstacle, and shows the matching margin.
- Clicking a trace time moves the scene there. Use exported event identities rather than calculating all-pairs feasibility in the browser.
- Use instanced agents, restrained path opacity, and source-consistent safety geometry.
- Choose one clear documented 3D case for main inspection; show 2D scaling statically. Other scenes may be separate slides/backups rather than a scene/count dashboard.
- Fallback: selected trajectory frames, critical-encounter detail, and full clearance curves.

Source candidates are 2D antipodal M=4,8,16,32,64,128; positional room M=100; sphere M=16/128. This is not a requirement to export every case. Do not borrow analogous 2D metrics for 3D scenes or attach amortized latency to per-instance trajectories.

Distinguish pairwise distance from signed clearance relative to the safety threshold, and pairwise constraints from obstacle constraints. Cost gap is relative to its stated lower bound, not an unknown constrained optimum. Finite-grid evaluation supports sampled feasibility, not a continuous-time certificate. Interpolated playback is display-only.

An exported amortized failed case can reuse this renderer in backup material; exporting all test trajectories is not required for the aggregate feasibility table.

### Chapter 5 — ETIterationPlayback (conditional)

- [x] (conditional) ETIterationPlayback: interactively scrub inference iterations while updating reconstruction, error, and any available test-time energy traces.

First inspect the saved sequence. If three or four frames explain the emergence of structure, use a static progression. Enable playback only when intermediate changes strengthen the explanation and real frames exist.

Scrubbing iteration n updates reconstruction/error panels and the cursor on actual test-time energy/error traces when available. Ground truth and the original observed-patch overlay remain fixed references; do not imply observed latent tokens are clamped unless the implementation does so. Only tokens evolve at inference, not model weights.

Distinguish iteration from physical time. Do not substitute training loss for energy or claim strict monotonic descent without checking. No training-coverage selector belongs here.

### Chapter 6 — RFormerSpatialInspector (conditional)

- [ ] (conditional) RFormerSpatialInspector: interactively rotate or slice synchronized reference, prediction, and error fields when a fixed view hides meaningful geometry.

Start with fixed thesis slices and native-coordinate plots. Enable inspection only when a meaningful feature is hidden by a fixed view and suitable geometry/predictions exist.

Use either synchronized reference/prediction/error point-cloud rotation or one shared slice-position control. Keep coordinates and color scales aligned. Inspect geometry within one sample/protocol; do not change dataset, model, density, or noise. No cursor-driven model inference.

Do not reshape irregular points into a fictitious grid. Document any display interpolation, validity mask, and reference type. Metrics remain on the native evaluation domain. Distinguish raw DPD targets from time-averaged blood-flow references.

## 4. Scientific evidence rules

Figures cite sources; metrics identify definition, units, aggregation population, protocol, and relevant platform. Keep qualifications concise on slides and detailed in notes/inventory.

| Label | Meaning |
|---|---|
| tested | Documented experiment or verified reproduction under its protocol |
| exploratory | Real forward-pass investigation outside thesis experimental claims |
| illustrative | Schematic/display interpolation; no empirical badge attributed to the constructed state |
| projected / future | Motivation/outlook claim labels, not selectable model outputs |

Corrections and qualifications governing all exports:

- **SNN:** 0.229 rate, 0.692 floating point, 0.135 direct, 0.047 lower triangular K=50, and 0.005 K=500 are Poisson spiking DeepONet mean relative errors over 200 held-out samples after Savitzky–Golay smoothing (window 51, order 3). They are not scalar codec errors. Show forcing → encoded coordinates → solution. Source: Chapter 2, `tab:ch02:deeponet-encoding`.
- **Conversion:** distinguish ANN error, SNN-to-ANN conversion error, and error against a numerical reference. Calibration theory concerns floating-point conversion; fixed-point rounding is separate.
- **Loihi:** the thesis labels 0.0131 CPU, 0.0215 8-bit, and 0.0160 effective 16-bit as RMS field errors. Verify original normalization/units; do not export as relative L2. Effective 16-bit uses two 8-bit connections per weight. Show measured replication curves and the reported multi-chip transition near 70 replicas. Energy measurements exclude I/O; do not fabricate CPU energy or generic savings multipliers. Source: Chapter 3, `tab:conversion:loihi-accuracy` and hardware results.
- **RFG:** experimental parameter perturbations are described as Bernoulli; Gaussian threshold shifts in the weak surrogate are distinct. Label a Gaussian estimator schematic illustrative and verify the implemented sampling convention before quantitative claims. RFG avoids reverse mode, not derivatives; training-energy savings are not measured here. Include BP/global/layerwise results. Source: Chapter 4, `sec:rfg:estimator`, `tab:rfg:poisson`, and limitations.
- **ET:** 25/50/75/100% coverage changes the training sequence and trained model, not inference context or spatial masks. Full ET does not win every module-ablation metric. PINN can have lower pointwise velocity error yet lose high-wavenumber energy. Sources: Chapter 5, `sec:et:fidelity`; Appendix B, `tab:app-et-temporal`, `tab:app-et-module`.
- **RFormer:** keep density/noise ablations separate unless joint experiments exist. Retain dataset-specific protocols and uncertainty. Blood flow uses raw and averaged references and has nearly tied leading baselines. No matched ET–RFormer head-to-head is established. Source: Chapter 6, experiments and synthesis.
- **OCFormer:** approximately 220-ms amortized inference concerns held-out rotations, with 100% feasibility at M=8 and 75% at M=16. Per-instance optimization takes approximately 20 minutes; transfer takes seconds. No extension to arbitrary boundaries, variable M, or amortized 3D room results is implied. The latent map concerns state and costate and is motivated by a diffeomorphism assumption; an overlay does not prove it. Source: Chapter 7, `tab:oc:amortized` and limitations.

## 5. Data contracts proportional to the visualization

This section replaces the previous per-widget contracts. No JSON is required for every static figure. Use **schema version 2** for the revised dynamic bundle; reject old manifests instead of silently interpreting them under this contract.

### Collection workspace and provenance

Each dynamic plot has a collection package under `data/raw/{chapter}/{plot}/`. The plot directory is the reusable code and provenance unit; each dataset, case, or configuration is a separate run below `runs/{case_id}/{run_id}/`, including plots that currently need only one run. The package contains a standalone `collect.py`, a Slurm `job.sh`, a short README, a tracked run list when multiple runs are possible, and a raw payload for every run. Explicit ignore rules must exclude payloads and logs while collection code, launchers, run definitions, metadata schemas, and README files remain reviewable.

Use this layout for every collected plot:

```text
data/raw/ch03/conversion_over_t/
  collect.py
  job.sh
  README.md
  runs.yaml                         # Case/run/configuration index
  runs/
    helmholtz_l3/
      T064_max_prefix/
        metadata.json
        payload.h5
  logs/
    helmholtz_l3/T064_max_prefix.*  # Ignored
```

`collect.py` accepts a stable `case_id`, `run_id`, source/config arguments, and an output directory. `job.sh` can submit one run or a Slurm array from `runs.yaml`; it must write each result to its own run directory and fail if that directory is already populated unless an explicit overwrite mode is used. A run directory is the atomic collection unit, so a failed or partial run cannot be mistaken for a complete plot dataset.

Collectors import source repositories read-only and write only to their collection directory or an explicitly configured staging directory. They must not patch or generate files inside the source model repository. Submit `job.sh` with `sbatch`; the script uses `srun` inside the allocation, activates the required environment explicitly, and writes separate stdout/stderr logs for each case/run.

Each run's metadata records the `case_id`, `run_id`, source repository path, commit and dirty state, configuration and checkpoint hashes, environment/interpreter, Slurm job and resource request, sample IDs and split, normalization and units, tensor shapes, collection command, and payload checksum. Raw captures are immutable inputs to the exporter. Derived prefix outputs, errors, and browser assets are written to `data/staging/` and `public/data/`; the browser never reads `data/raw/`.

### Static assets

Use browser-ready SVG/PNG figures under `public/figures/chXX/`. Existing publication figures need provenance and readable adaptation, not checkpoints or raw prediction exports. Convert PDF inputs during preparation.

For redrawn plots, keep only required CSV/JSON plot inputs in `figure_sources/{chapter}/{plot}/` and deterministic plotting scripts in `scripts/`. These are build-time sources, not runtime tensors. Record every slide asset in `docs/data_inventory.csv`: ID, chapter, treatment, source/thesis label, path, metric/protocol/platform, processing notes, and collection status. No runtime `claim_evidence.json` is required.

Use `figure_sources/{chapter}/{plot}/` for small static inputs and `data/raw/{chapter}/{plot}/runs/{case_id}/{run_id}/` for collected dynamic evidence. This keeps dataset-specific static inputs, raw model outputs, and browser-ready states separate while giving every plot a stable chapter/plot identity.

### Dynamic manifest and envelope

Only enabled dynamic assets appear in `public/data/manifest.json`. The manifest has `schema_version: 2`, `presentation_id`, `generated_at`, `generator_commit`, and `assets[]`. Each entry has:

- `asset_id`, `chapter`, `component`, `path` relative to the manifest, `default_state`, `fallback_path`, and `sha256`.
- `status`: required for SMS/conversion/swarm; optional for an enabled conditional inspector.

Write the manifest last. Each mounted component references exactly one listed asset. Disabled conditional inspectors have no data dependency or placeholder entry.

Dynamic files contain `schema_version`, `asset_id`, `chapter`, `title`, `generated_at`, `source`, `units`, `defaults.state_id`, and `data.states[]`. Source records thesis refs, source repository/run/config identity, raw collection path and checksum, reproduction notes, and processing. States have `id`, `case_id`, `run_id`, `status` (tested/exploratory/illustrative), `protocol_id`, `payload`, and optional metrics. A derived state may instead include `source_runs[]` when it combines multiple raw runs, such as branch and trunk captures. Metric records specify name, value, unit, definition, aggregation, source ref, and relevant platform. Illustrative states have no empirical metrics. One browser asset may aggregate several run directories into selectable states, but every state must point back to exactly one raw run or an explicitly documented derived combination.

Numeric tensors use explicit `dtype`, `shape`, `order: C`, and flat `values`, with explicit coordinates/axes. Reject NaN/Infinity. Null is for unavailable scalar measurements, not missing required arrays. Store trajectory time in seconds, inference timing in milliseconds, fractions as decimals, and energy in stated units. JSON is the initial transport; binary requires a documented byte-order/length/loading extension.

### Required payloads

| Asset / component | Required payload |
|---|---|
| `ch02/sms_longtime_rollout.json` / SMSRollout | `time`, `reference_state`, `one_step_state`, `cascade_state`, `one_step_error`, `cascade_error`, `training_end_time`, coordinates/axes, `encoding_horizon_steps` |
| `ch03/conversion_over_t.json` / ConversionOverT | `loop_step`, `simulation_length_T`, sample IDs, subnet/final-layer identity, `step_spikes`, `prefix_output`, ANN output, numerical reference, per-step errors, output axes/units |
| `ch07/ocformer_swarm_3d.json` / DroneSwarm3D | `time`, `positions` [time, agents, dimension], stable `agent_ids`, benchmark/regime/dimension, radius convention, obstacles with IDs/types/geometry, `clearance_traces`, `critical_events` |

SMS arrays share a time axis; state tensors are [time, state_dimension] or explicitly described field geometry. Document error definitions and reference-fed versus recursive evaluation.

For conversion, `step_spikes` is the emitted output of the final `SpikeModule` at each internal loop step. Define `prefix_output[t]` as the cumulative emitted output through step `t`, divided by `t + 1`; this is the output returned by the converted model at that prefix length. Membrane-potential traces are diagnostic and are not the decoded model output. A single run with maximum `T` supplies the prefix history. A separately configured `T` is a separate conversion/evaluation state because `T` is fixed during model construction and threshold calibration. For DeepONet, reconstruct the full output from the branch/trunk prefix outputs using the same composition as the source model; for POD cases, use the fixed basis and mean-field reconstruction.

Swarm traces include constraint type, units, threshold convention, and values. Critical events identify time, agent/obstacle IDs, clearance, and trace reference. Record the evaluation grid and checked constraints. Preserve positions at actual critical-event times even when display arrays are thinned. Cost, cost gap, and feasibility are separate metrics; omit unavailable measurements. Controls and speed/boundary diagnostics are optional when relevant.

### Conditional payloads

- `ch05/energy_hopfield_steps.json` / ETIterationPlayback: fixed sample/mask, coordinates, observed-patch mask, input/truth, frames with explicit iteration, reconstruction, and optional test-time energy/error. Apply evidence status/provenance to frames; interpolations are not actual iterations.
- `ch06/rformer_spatial.json` / RFormerSpatialInspector: fixed sample/dataset/protocol, sensor coordinates/values, geometry type (point_cloud or grid), coordinates, reference, prediction, error, component, shared color limits. Point fields use [points, channels]; grids specify axes/shape. Document interpolation, validity masks, reference type, and any connectivity.

Static comparisons and ablations have no mandatory dynamic schema. Attention weights and continuous diffeomorphism morphs have no export requirement.

## 6. Runtime and defense ergonomics

Use Slidev/Vite/Vue 3, KaTeX, locally bundled Latin Modern/Inter fonts, and a high-contrast Brown APMA theme. Markdown and static figures handle most slides. Three.js with OrbitControls handles swarm geometry; Canvas/SVG handles rollout views and linked traces. Add a chart library only if those traces require it.

All model computation happens before the defense. Browser code loads local assets once, validates once, converts tensors to typed arrays, and renders deterministic playback. No model inference, cluster paths, external fonts/CDNs, or remote requests.

Share a figure frame, cached loader, playback controller, and linked trace primitive. Keep arrays outside deep Vue reactivity. Synchronize by scientific time/iteration, not independent clocks. Isolate widget pointer events, retain keyboard accessibility and slide navigation, pause inactive slides, and dispose of rendering resources.

Open each view in an informative static state. Use fallback figures for print/PDF. Required data failures block release; enabled optional failures show their approved static alternative. The PDF provides JavaScript-independent delivery; a Vue fallback alone does not handle complete JavaScript failure.

## 7. Build and readiness

Commands are proposed until implementation. Define validation, build, and PDF scripts, pin dependencies, and install export browsers before going offline.

```bash
cd presentation
npm ci
npm run validate:assets
npm run build
npm run export:pdf
./present.sh
```

The launcher serves prebuilt dist/ on loopback using a preinstalled server, verifies readiness, opens the audience view, and remains alive until explicitly stopped. It must neither download tools nor exit when the browser-opening command returns. Test presenter routes and dual displays in the built site.

Release checklist:

- [ ] (required) Main slides and backups retain thesis order.
- [ ] (required) Scientific comparisons are readable side by side.
- [ ] (required) SMS/swarm sequences, linked traces, critical events, and fallbacks validate.
- [ ] (required) Conditional decisions are recorded; static decisions leave no release blockers.
- [ ] (required) Metrics, smoothing, normalization, units, protocols, and references are verified.
- [ ] (required) Loading, memory, playback, and camera behavior are tested on the defense laptop.
- [ ] (required) Every PDF page and dynamic fallback is visually inspected.
- [ ] (required) Full talk works without Wi-Fi or cluster mounts.
- [ ] (required) Presenter/audience displays, optional-data failure, and WebGL failure are tested.
- [ ] (required) Built site, PDF, figures, and launch instructions are on laptop and backup media.
