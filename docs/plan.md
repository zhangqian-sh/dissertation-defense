# Presentation data collection and implementation plan

Implement [design.md](design.md) using the source locator and proposed layout in [file_structure.md](file_structure.md). This plan replaces the earlier per-widget/Tier 1–3 workflow. Paths and commands below describe future implementation; only the documentation currently exists.

The deliverable is a mostly static, offline Slidev defense with **three required interactive plots: SMS/SDON rollout and T approximation, conversion output over T, and OCFormer trajectory inspection**. ET iteration playback and RFormer spatial inspection are conditional. Slides always follow Chapters 1–8 in thesis order.

## 1. Audit sources and classify collection work

Resolve the candidate paths in file_structure.md before reading artifacts. If both paths are distinct checkouts, compare commits/configurations/run metadata; do not silently mix code and results. Use targeted file searches and small metadata reads before opening large arrays.

Begin with tracked thesis chapters, figures, tables, and Appendix B. Trace ambiguous results to source manuscripts or experiment repositories. Paper files and archives remain read-only references. The locator has no dedicated Loihi measurement repository: trace Chapter 3 through `papers/SNN_05_Nice2024_hardware` and its logs. Missing hardware logs do not prevent using a correctly cited existing figure, but do prevent inventing additional measurements.

Create `docs/data_inventory.csv` with one row per slide figure or enabled dynamic case:

- Asset ID, chapter/slide, static/required-dynamic/conditional treatment, scientific question, and source thesis label.
- Input/output path, source repository/run/config identity when applicable, processing/reproduction command, and collection status.
- Dataset/sample/split, normalization, observation protocol, smoothing, metric definition/units/aggregation, and relevant platform.
- Required fields already available, missing inputs, fallback source, and validation result.
- For conditional views: evidence reviewed, information lost in static panels, decision, and reason.

Use `located`, `needs_adaptation`, `needs_export`, `needs_rerun`, and `unavailable` as collection statuses. They are distinct from tested/exploratory/illustrative evidence labels. Record a source commit and dirty-state note, checkpoint hash, seed, and environment only for work that actually uses those artifacts; static figure reuse does not require recovering the training environment.

### Per-plot collection packages

Put each dynamic plot's collection work under `presentation/data/raw/{chapter}/{plot}/`. Keep one reusable collector per plot and put every dataset, case, or configuration in a separate run directory:

```text
presentation/data/raw/{chapter}/{plot}/
  collect.py
  job.sh
  README.md
  runs.yaml                         # Tracked case/run/configuration index
  runs/{case_id}/{run_id}/
    metadata.json
    payload.h5 or payload.npz
  logs/{case_id}/{run_id}.*          # Ignored
```

- `collect.py`: standalone source adapter that imports the source repository read-only, accepts `case_id` and `run_id`, and writes one complete raw capture to that run directory.
- `job.sh`: Slurm batch wrapper with all `#SBATCH` directives before executable commands, explicit environment/interpreter setup, `srun python collect.py`, and separate stdout/stderr logs. It may use a job array to execute entries from `runs.yaml`.
- `README.md`: source, input, output, run-selection, and reproduction instructions.
- `runs.yaml`: stable case/run/configuration parameters and source mapping when the plot has more than one capture; it is also the input for a Slurm array when useful.
- `metadata.json`: per-run source commit and dirty state, configuration/checkpoint hashes, environment, Slurm job/resource information, sample IDs/split, normalization, units, shapes, command, and checksum.
- `payload.h5` or `payload.npz`: immutable per-run raw capture; explicit ignore rules must exclude payloads and logs while the collector, launcher, run index, README, and metadata schema remain tracked.

Use the same package contract for required and enabled conditional plots. A single-case plot still uses `runs/{case_id}/{run_id}/`, which keeps the exporter and provenance logic uniform. Collectors must not modify the source model repository or write checkpoints there. Before the first submission, add and verify explicit ignore rules for raw payloads and logs. Write derived prefix outputs, error arrays, and browser-ready files to `presentation/data/staging/` and `presentation/public/data/` through the exporter. The browser never reads `presentation/data/raw/` directly.

### Three collection paths

1. **Reuse:** copy a readable thesis figure into the chapter's presentation figure directory, convert PDF to browser-ready SVG/PNG, and retain citation/caption qualifications.
2. **Redraw:** collect the small table/curve inputs needed for a clearer static comparison. Preserve uncertainties and protocols; keep CSV/JSON inputs in figure_sources/ and deterministic plotting code in scripts/. Do not request full prediction tensors merely to redraw a curve.
3. **Dynamic export:** run the per-plot collector in its Slurm allocation and collect aligned arrays and event metadata only for required or explicitly enabled conditional inspectors. Prefer saved outputs; reproduce documented evaluation only when necessary. Export selected run directories through staging into the versioned browser bundle, preserving one browser state per case/run. If a state combines runs, record every input run in its source metadata.

Do not retrain models simply to add interaction. If required outputs cannot be recovered, document the gap and provide a cited static fallback; report that the required interaction remains incomplete until the scope is explicitly revised. A static decision for a conditional view is complete, not blocked.

Run expensive inference, training, or large processing in Oscar Slurm allocations, following the submit-slurm-jobs skill when executing that work. No computation is submitted by this documentation update. Keep model environments outside the browser/export validator.

## 2. Collect evidence in chapter order

| Chapter | Static content and minimum inputs | Dynamic collection |
|---|---|---|
| 1 | Thesis organization and contribution map from Chapter 1; source/metric references for closing reuse | None |
| 2 | Encoding rasters and matched Poisson solution panels; encoder error table with 200-sample statistics and smoothing caption | One SMS/SDON case: aligned physical time, reference, reference-fed one-step prediction, recursive prediction, both error traces, training boundary, geometry, encoding horizon, and selected T values |
| 3 | Calibration workflow/theorem interpretation; ANN/uncalibrated/calibrated fields; compact T=8/32/128 example where available; Loihi precision fields and measured replication curves | Conversion-over-T case: final-layer emitted spikes and cumulative prefix outputs recorded through T, with ANN/reference comparisons, per-step errors, and conversion protocol |
| 4 | Forward-JVP/global-layerwise schematic; matched BP/RFG predictions and error distributions, including Poisson and a larger-scale limitation example | None; schematic reveals need no forward-pass exports |
| 5 | Patch/token workflow, representative refinement frames, ET/PINN field/error/spectrum comparison and inference timing; module/temporal ablations for backup | Inspect saved iterations first; export full sequence only if ET playback passes the decision gate |
| 6 | Token roles/mask/chunking schematic; vortex density/noise small multiples and curves; jet baseline fields/spectra; qualified weather/blood examples | Review existing geometry/slices; export native spatial arrays only if a fixed view hides an important result |
| 7 | Latent/physical overlay and physics-informed training diagram; OCFormer/SympOCNet scaling; regime timing, cost, and feasibility table | One clear documented 3D trajectory with geometry, constraints, clearance traces, and closest-event metadata; additional cases only when needed |
| 8 | Reuse opening map and verified chapter metrics for synthesis and limitations | None |

Use existing plots when their scientific comparisons are already clear. Redraw only to improve projection readability or assemble an otherwise missing side-by-side comparison. Static additions are substantive requirements, not lower-priority substitutes for dashboards.

### Evidence checks before rendering

Apply design Section 4 and verify exact thesis/source references:

- SNN error anchors describe smoothed Poisson operator predictions, not scalar codec error. Keep the same forcing sample across displayed encoder outputs.
- Conversion-over-T records the final `SpikeModule` emitted output at each internal loop step and computes the cumulative prefix output returned at each step. Keep ANN output, numerical reference, and per-step conversion errors distinguishable. Do not use membrane potential as the decoded output, conflate internal T with physical time, or imply convergence without evidence.
- Loihi error anchors are labeled RMS in the thesis; resolve source normalization and units rather than relabeling relative L2. Keep both precision curves visible and annotate replica/chip transitions. Energy scope excludes I/O.
- RFG parameter sampling and weak-surrogate threshold noise are distinct. Explain derivatives carried by the JVP and show BP/global/layerwise accuracy; do not claim measured training-energy savings.
- ET iteration changes tokens with fixed weights. Temporal training coverage compares separately trained configurations. Keep pointwise error and spectral fidelity together; do not claim full ET wins every ablation metric.
- RFormer density and noise curves are separate experiments unless joint results exist. Retain raw versus averaged blood references, near-tied baselines, dataset-specific masks, and error-bar definitions.
- OCFormer approximately 220-ms amortized inference applies to held-out rotations with 100% feasibility at M=8 and 75% at M=16. Keep these metrics separate from per-instance 3D playback and label the cost lower bound.

If thesis text, a plotted figure, and raw measurements disagree, record and resolve the discrepancy before publishing the affected claim. Never overwrite an exported value with a target number merely to pass validation.

## 3. Resolve the two conditional views

### ET gate

Inspect available reconstructions through the 12 inference iterations and create a candidate three/four-frame static progression. Enable ETIterationPlayback only if substantial intermediate structure is lost and genuine frames are accessible. Do not rerun merely to generate a decorative energy curve.

When enabled, export fixed input/truth/mask and reconstruction frames with iteration IDs. Include actual test-time energy and error traces where available. Do not substitute training loss or interpolate missing frames as tested iterations. A static progression remains the required fallback.

### RFormer gate

Inspect the thesis's fixed slices and native-coordinate views for the chosen case. Enable RFormerSpatialInspector only if rotation or moving a slice reveals a scientifically relevant feature that fixed panels obscure.

Choose one operation: synchronized point-cloud rotation or synchronized slicing. Collect native coordinates, reference/prediction/error, sensors, component, color limits, and required geometry/mapping. Record interpolation and validity masks. Do not infer 3D values from a published 2D image. If there is no material benefit, keep static figures and skip the component/export entirely.

## 4. Prepare the required dynamic bundle

Use design Section 5's **schema version 2**. Implement the required SMS/SDON, conversion-over-T, and swarm schemas first; add conditional schema branches when enabled. Static figures are validated through the inventory and slide references, not forced into tensor envelopes.

Implement one standalone source adapter under each selected plot's `data/raw/{chapter}/{plot}/` directory. Give every capture a stable `case_id` and `run_id` with protocol/config provenance, and write it to `runs/{case_id}/{run_id}/`. Use a tracked run index when a plot has multiple datasets or configurations; a Slurm array may execute those entries with the same collector. Preserve metric precision at source resolution before float32 display conversion or thinning. Keep the adapter, `job.sh`, run index, README, and metadata schema tracked; keep raw payloads and logs under explicit ignore rules.

For SMS/SDON, align one-step/cascade/reference arrays and error traces on physical time. Record the train/extrapolation boundary, distinguish simulation horizon K from the selected T values, and document any resampling.

For conversion, use a single forward pass at the maximum configured `T` and attach a forward hook to the final `SpikeModule`, following the existing `capture_snn_traces` pattern. Save its emitted `spikes` at every loop step and compute `prefix_output[t] = cumsum(spikes[:t + 1]) / (t + 1)`. The prefix at `T` must equal the output returned by `SpikeModel.forward()`. Save the ANN output, numerical reference, per-step errors, loop index, subnet/final-layer identity, and conversion precision/protocol. Do not rely on the current `save_intermediate` path or membrane-potential traces as the output history. For DeepONet, capture branch and trunk prefixes separately and reconstruct the full output with the source model's composition; for POD cases, reconstruct from the fixed basis and mean field. Internal loop steps are separate from physical time.

Do not emulate different configured `T` values by truncating a model calibrated for another `T`. A maximum-`T` run stores all valid prefix outputs for that conversion. If the study compares separate configured `T` values, run separate conversions/evaluations and store each as a distinct `case_id`/`run_id` state with its own thresholds, checkpoint/config hashes, and payload.

For swarms, preserve stable agent IDs and actual obstacle geometry. Compute/collect constraint diagnostics offline using the original evaluation grid and definitions. Export the identities and exact times of closest encounters plus the corresponding positions so thinning does not hide the event. Distinguish pairwise margin, obstacle margin, and aggregate feasibility. Do not certify continuous-time safety from playback samples.

Generate into a staging directory from the immutable raw captures, render fallback figures from the same evidence, then write manifest.json last. Validate before replacing the published bundle and preserve the previous valid bundle. Resolve manifest paths under public/ including fallback references; reject traversal outside public/. Hash raw inputs and release inputs.

Proposed exporter/validator interfaces from the repository root:

```bash
python presentation/scripts/export_defense_assets.py --out presentation/public/data
python presentation/scripts/validate_defense_assets.py presentation/public/data/manifest.json
```

The exporter should support configured raw roots, source paths, and explicit asset filters. Run expensive collectors inside allocations; final packaging can read their prepared outputs. No all-chapter model-export sweep is required.

Validate unique asset, case, run, and state IDs; versions; tensor shapes/lengths; finite values; physical-time and loop-step alignment/order; conversion prefix consistency; event-to-trace consistency; default IDs; source refs; and units. Check required run payload availability and informative fallback paths. Missing scalar metrics display unavailable, not zero. Conditional absence is valid when disabled; enabled optional failure uses the approved fallback.

## 5. Implement the mostly static deck

Build the complete Chapter 1–8 Markdown deck before extending optional interactions. Use Slidev/Vite/Vue 3, KaTeX, local fonts, the Brown APMA theme, and citations/notes. Pin compatible dependencies during implementation.

Most slides need no custom Vue component: use images, aligned panels, tables, and ordinary reveals. Keep parallel comparisons visible together. Avoid a general selector framework, metric dashboard, attention hook collection, or one component per scientific topic.

For required dynamic figures implement:

- Shared FigureFrame with default image, loading/error state, caption, and export fallback.
- Cached local asset loader and schema types, converting arrays once and keeping them outside deep Vue reactivity.
- Shared playback controller and linked trace renderer.
- Chapter 2 SMSRollout / SDON-SMS: physical-time controls, synchronized prediction/reference/error views, training marker, and selected-T stepwise approximation.
- Chapter 3 Conversion over T: loop-step control or playback over `prefix_output`, per-step final-layer spike capture, and distinct ANN/reference/error comparisons. The browser receives the staged prefix output, not raw membrane-potential traces.
- Chapter 7 DroneSwarm3D: instanced geometry, synchronized time/trace, camera/reset, and exported closest-event highlighting.

Browser code only renders exported evidence; it performs no model inference or feasibility certification. Three.js handles 3D; Canvas/SVG is sufficient initially for rollout/trace views. Avoid extra chart dependencies unless justified by the actual implementation.

Pause inactive slides, dispose of listeners/resources, isolate widget pointer events from deck navigation, and retain accessible keyboard controls. Script a short demonstration sequence for each dynamic slide. Put free inspection controls within reach for questions without making the talk depend on them. The conversion plot's internal loop controls must remain distinct from physical-time controls.

### Milestones and completion gates

| Milestone | Work | Exit condition |
|---|---|---|
| A — Source audit | Inventory figures/tables and selected dynamic runs in chapter order | Core evidence mapped; missing data recorded without requesting unnecessary checkpoints |
| B — Static defense | Assemble all chapters, improve side-by-side plots and method diagrams, include static alternatives for sequences | A complete scientifically coherent talk can be given from static slides |
| C — SMS/SDON interaction | Export/validate one rollout; implement shared playback and SMS/SDON views | Physical time, histories, train boundary, T approximation, errors, and fallback agree |
| D — Conversion-over-T interaction | Export/validate the per-loop-step SNN outputs; implement the T playback/inspection view | Output evolution, ANN/reference comparisons, conversion protocol, and fallback agree |
| E — OCFormer interaction | Export selected scene/critical events; implement linked geometry and clearance inspection | Scrubbing/camera/closest-encounter behavior reveals the intended evidence |
| F — ET decision | Review ET frames; implement ETIterationPlayback only if the decision gate passes | ET decision documented; static progression counts as complete when playback is not enabled |
| G — RFormer decision | Review RFormer geometry; implement RFormerSpatialInspector only if the decision gate passes | RFormer decision documented; static slices count as complete when inspection is not enabled |
| H — Release rehearsal | Build, PDF export, offline laptop and dual-display testing | Required plots and all scientific slides work; backups are usable |

Milestones do not reorder slides. Additional backups are grouped in thesis chapter order.

## 6. Verify and release

Use targeted contract tests for malformed tensors, invalid defaults, missing required/optional assets, and mismatched event/time/agent references. Browser checks cover linked scrubbing, loop-step/T playback, closest-event highlighting, camera reset, pause on slide exit, navigation isolation, fallback behavior, and PDF capture. Do not create selector tests for removed widgets.

Visually compare all adapted static figures against their sources. Inspect captions, uncertainties, scales, reference types, and every exported PDF page. No LaTeX build is needed for a docs-only update; compile affected thesis deliverables if their sources are changed in future work.

Measure actual laptop cold-load time, memory, and playback responsiveness for selected sequences, including the conversion-over-T view. Reduce rendering geometry where justified while preserving full-resolution scientific metrics and critical events. Move large arrays to binary only if measurements justify the added schema/loader complexity.

Define these package scripts during implementation; build runs asset validation first:

```bash
cd presentation
npm ci
npm run validate:assets
npm run build
npm run export:pdf
./present.sh
```

Install dependencies and export-browser binaries before disconnecting. present.sh must use a preinstalled local server on loopback, check dist/ and readiness, and remain alive until explicitly stopped. Avoid network-dependent npx downloads and premature shutdown after opening a browser.

Rehearse with Wi-Fi off and cluster mounts unavailable. Test audience/presenter routes, dual displays, missing optional assets, WebGL failure, and the PDF-only alternative. Ensure no CDN/font/API request is required.

Package the built site, manifest/hashes, static PDF, figures, and concise launch instructions on laptop and backup media. Keep raw run payloads and logs under the explicit `data/raw/` ignore rules, along with checkpoints, node_modules/, staging directories, and generated build/PDF products. Keep collection code, `job.sh` files, run indexes, metadata schemas, and README instructions reviewable. Run git diff --check and verify ignored/tracked files.

Completion requires the static scientific narrative in thesis order, three working required plots with fallbacks, explicit conditional decisions, and a rehearsed offline deliverable. It does not require the retired widget catalog or model exports for every chapter.
