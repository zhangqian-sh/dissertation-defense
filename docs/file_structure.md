# Presentation source locations and file structure

[design.md](design.md) defines scientific content, interaction scope, and data contracts. [plan.md](plan.md) defines collection and implementation. The presentation is mostly static. The dynamic scope has three required plots—SMS/SDON rollout and T approximation, conversion output over T, and OCFormer trajectory inspection—and two conditional plots: ET iteration playback and RFormer spatial inspection.

## Source repository locator

These are candidate locations from the original project locator, not verified interchangeable copies. Resolve symlinks and inspect commits/configs/run identities before combining code and results.

| Study | Candidate code root | Candidate data/project root |
|---|---|---|
| SDON | /users/qzhang64/Projects/SpikingNN/UNO | /users/qzhang64/data/qzhang64/Projects/SpikingNN/UNO |
| SMS | /users/qzhang64/Projects/SpikingNN/spiking_marching_scheme | /users/qzhang64/data/qzhang64/Projects/SpikingNN/Spiking-Marching-Scheme |
| Conversion | /users/qzhang64/Projects/SpikingNN/UNO | /users/qzhang64/data/qzhang64/Projects/SpikingNN/UNO |
| RFG | /users/qzhang64/Projects/SpikingNN/RFWG-SpikingNN | /users/qzhang64/data/qzhang64/Projects/SpikingNN/RFWG |
| Energy Transformer | /users/qzhang64/Projects/OperatorLearning/ETRO | /users/qzhang64/data/qzhang64/Projects/OperatorLearning/ETRO |
| RFormer | /users/qzhang64/Projects/OperatorLearning/RFormer | /users/qzhang64/data/qzhang64/Projects/OperatorLearning/RFormer |
| Optimal Control | /users/qzhang64/Projects/OptimalControl/OCFormer | /users/qzhang64/data/qzhang64/Projects/OptimalControl/OCFormer |

No dedicated Loihi hardware repository is listed. Trace measurements through Chapter 3 and papers/SNN_05_Nice2024_hardware before seeking new exports. Treat source repositories, ignored manuscripts, and archives as reference inputs.

## Start with thesis evidence

| Chapter | First sources | Extra experiment access needed |
|---|---|---|
| 1 | thesis/chapters/ch01-introduction/ and thesis/images/ch01/ | None for static organization map |
| 2 | thesis/chapters/ch02-spiking-foundations/ and thesis/images/ch02/ | SMS/SDON sequence arrays and selected-T approximation data; encoding plot inputs only if redrawing |
| 3 | thesis/chapters/ch03-conversion-hardware/ and thesis/images/ch03/ | Conversion-over-T output traces; small calibration/hardware curve data if existing figures need adaptation |
| 4 | thesis/chapters/ch04-forward-gradient/ and thesis/images/ch04/ | Matched comparison plot inputs if redrawing; no required gradient demo export |
| 5 | thesis/chapters/ch05-energy-reconstruction/, thesis/images/ch05/, and Appendix B | Conditional iteration sequence only after reviewing static frames |
| 6 | thesis/chapters/ch06-rformer/, thesis/images/ch06/, and Appendix B | Conditional native spatial arrays; no required attention-weight capture |
| 7 | thesis/chapters/ch07-ocformer/ and thesis/images/ch07/ | Selected trajectory, geometry, clearance traces, and critical events |
| 8 | thesis/chapters/ch08-summary/ and earlier presentation figures | Reuse verified evidence |

Use thesis/references.bib for citation identity. A static figure can be sourced from a published artifact without recovering a checkpoint. Browser assets must be copied into presentation/public/; no runtime links to papers/, source repositories, or cluster mounts.

## Proposed presentation layout

Only docs/ currently exists. Add files as needed during implementation, preserving Chapter 1–8 slide order.

```text
presentation/
  docs/
    design.md
    file_structure.md
    plan.md
    data_inventory.csv              # Future figure/export provenance and decisions
  data/
    raw/
      ch02/sms_sdon/                # Collector plus runs/{case_id}/{run_id}/
      ch03/conversion_over_t/       # Collector plus runs/{case_id}/{run_id}/
      ch05/et_iteration/             # Same layout if enabled
      ch06/rformer_spatial/          # Same layout if enabled
      ch07/drone_swarm_3d/           # Collector plus runs/{case_id}/{run_id}/
    staging/                         # Derived validation/export outputs; ignored
  slides.md                         # Master assembly in thesis order
  slides/
    ch01-introduction.md
    ch02-spiking-foundations.md
    ch03-conversion-hardware.md
    ch04-forward-gradient.md
    ch05-energy-reconstruction.md
    ch06-rformer.md
    ch07-ocformer.md
    ch08-summary.md
  components/
    shared/                         # Figure frame, playback, linked trace
    ch02/SMSRollout.vue              # Required
    ch03/ConversionOverT.vue         # Required
    ch07/DroneSwarm3D.vue            # Required
    ch05/ETIterationPlayback.vue     # Create only if enabled
    ch06/RFormerSpatialInspector.vue # Create only if enabled
  composables/                      # Cached asset loading and shared playback
  types/
  schemas/                          # Dynamic manifest/payload contract v2
  config/
    export_sources.example.yaml     # Logical run/source mappings
  figure_sources/
    chXX/{plot}/                    # Small CSV/JSON inputs for redrawn static plots
  scripts/
    export_defense_assets.py         # Only enabled dynamic assets
    validate_defense_assets.py
    render_figures.py                # Static plots and dynamic fallbacks
    exporters/                      # Shared raw-to-schema export helpers
    slurm/                          # Shared templates; plot job.sh files live with collectors
  tests/                            # Contract and essential browser behavior
  styles/
    apma-theme.css
    index.ts
  public/
    figures/chXX/                   # Main static and backup SVG/PNG figures
    fallback_figures/chXX/           # Approved dynamic default/static progression
    fonts/                          # Local font assets and license notices
    data/
      manifest.json
      ch02/sms_longtime_rollout.json
      ch03/conversion_over_t.json
      ch07/ocformer_swarm_3d.json
      ch05/energy_hopfield_steps.json # Conditional
      ch06/rformer_spatial.json       # Conditional
  package.json
  package-lock.json
  vite.config.ts
  present.sh
```

Each `data/raw/chXX/plot/` collection package contains one standalone collector, a Slurm `job.sh`, a short README, a tracked run/configuration index when needed, and one metadata/payload pair per `runs/{case_id}/{run_id}/` directory. Its payload files and logs must be ignored by explicit rules; the collector, launcher, run index, metadata schema, and README remain reviewable. The same package contract applies to required and enabled conditional plots. Collectors may import source repositories read-only and must write only to their collection directory or an explicitly configured staging directory.

For example:

```text
data/raw/ch03/conversion_over_t/
  collect.py
  job.sh
  README.md
  runs.yaml
  runs/
    helmholtz_l3/
      T064_max_prefix/
        metadata.json
        payload.h5                # Ignored by an explicit rule
  logs/
    helmholtz_l3/T064_max_prefix.* # Ignored by an explicit rule
```

`collect.py` is parameterized by `case_id` and `run_id`; `job.sh` may submit one run or a Slurm array from `runs.yaml`. Every run directory is an immutable raw capture with its own source/config/checkpoint provenance. The exporter can combine selected run directories into browser states, while the browser reads only `public/data/`.

Static plots do not need chapter-specific Vue components or browser JSON. The former claim-map, encoding, hardware, RFG, ablation, attention, regime, and diffeomorphism widget files are not implementation requirements.

Keep scientific figure sources separate from raw collection payloads, derived staging outputs, and browser-ready figures. Raw captures are immutable inputs to the exporter, not runtime assets. Store payloads, logs, checkpoints, node_modules/, dist/, and release PDFs outside tracked source or under explicit ignore rules. Release artifacts are packaged for the defense, not committed unless requested.
