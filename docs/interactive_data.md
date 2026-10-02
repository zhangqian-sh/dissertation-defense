# Interactive plot data handoff

The entry point is `public/data/manifest.json`, schema version 2. Each of the
three required components has one case/run state. JSON tensors have explicit
dtype, shape, C order and flat values. Paths in the manifest are relative to
the manifest; fallback paths start at the public web root. Load assets through
the manifest, not a hardcoded release directory. Everything needed to render
the plots is local to `public/`; source cluster files are not runtime inputs.

| Component | State | Data |
|---|---|---|
| SMSRollout | `heat_triangular--saved_K100` | 100 physical frames, 101 spatial points, reference/one-step/cascade, both error traces, training boundary |
| ConversionOverT | `helmholtz_l1_k15--saved_T064_prefix` | 64 internal steps, 24 emitted POD coefficients, reconstructed fields on 1600 mesh nodes, fixed POD basis/mean/scales, ANN and numerical reference, separate errors |
| DroneSwarm3D | `ball_3d_M16--saved_lbfgs` | 200 original frames over 10 seconds, 16 agents in 3D, sphere geometry, three diagnostic traces, exact event indices/identities/positions |

## Scientific display rules

SMS uses the documented heat case with the triangular initial condition. Its
first two frames are encoded initial histories, not predictions. The time axis
is `reference_index * 0.00004 s`, with every tenth reference frame retained;
the final displayed frame is at 0.0396 s. Show the training boundary at 0.032 s.
Errors are unsmoothed relative discrete L2 over all spatial nodes. The growing
relative error must remain visible; do not label it negligible or substitute
the Poisson encoding table's errors. The source FDM endpoint stencil is retained
even though the thesis writes ideal zero Dirichlet boundaries.

The main SMS slide shows only the saved predictions and accumulated errors,
linked by physical-time playback and scrubbing. K=100 is the saved model's
spike horizon. Historical selected-T codec arrays remain in the archived
payload for provenance but are not displayed or selectable in the deck.

Conversion uses a documented saved Helmholtz POD evaluation, marked
**exploratory** relative to thesis claims. `loop_step` is zero-based; show
prefix length `loop_step + 1`. `step_spikes` contains signed, weighted emitted
outputs from the final branch SpikeModule, not binary indicators or membrane
potential. `prefix_output` is the cumulative mean of those coefficients.
`field_prefix_output` is the solution to display:

```
pod_mean + (prefix_output * coefficient_scales) @ pod_basis.T
```

Use the supplied triangular mesh connectivity; field and reference share native
coordinates. Keep ANN, numerical reference and their two error curves distinct.
T=64 is one configured/calibrated run. Earlier prefixes do not represent models
calibrated at smaller T. The error curve is not strictly monotone. Saved final
branch and full-field outputs provide independent prefix consistency checks.

OCFormer uses the per-instance L-BFGS trajectory, with no amortized latency or
2D cost claims attached. Agent radius is 0.02 for pairwise collision geometry;
the sphere of radius 0.1 is an **agent-center exclusion zone**, not a solid
obstacle inflated by the agent radius. Position units are benchmark units;
the source does not establish a physical meter calibration. Preserve agent IDs.

The source pair constraint is `sqrt(distance² + 1e-10) - 0.04` (length), and
the sphere constraint is `distance_to_origin² - 0.1² + 1e-10` (length squared).
The additional sphere distance margin is a geometric length diagnostic; do not
put the squared constraint and length margins on the same unlabeled axis.
Each closest event has its exact saved frame, time, agent/obstacle IDs and
positions. Do not recompute events from interpolated playback. Feasibility
means the two position constraints on the 200 saved frames only; it is not
a speed, boundary-error, or continuous-time certificate.

## Reproduction and verification

Each package under `data/raw/chXX/{plot}/` contains its collector, Slurm
launcher and run index. Raw payloads and logs are explicitly ignored; metadata
is reviewable. Existing captures are immutable and cannot be overwritten.
The capture reads saved numerical outputs only; no training or model inference
is necessary. Current audited code identities and dirty states are recorded
separately from unknown historical training commits.

Run from `presentation/` after collecting all three packages:

```bash
mkdir -p data/staging
sbatch scripts/export_assets_job.sh
```

The export launcher uses the explicit OCFormer environment only for NumPy,
h5py, PyYAML and Matplotlib. The validator has no Torch/JAX dependency.
`scripts/validate_defense_assets.py public/data/manifest.json` checks tensor
contracts, raw correspondence, hashes, physical time, prefix reconstruction,
error definitions, event identities and fallback paths. Run numerical checks
in an allocation. The launcher's test suite also corrupts selected fields to
verify that bad time axes, prefixes, events and nonfinite values are rejected.

Export writes staging files, validates them, copies an immutable timestamped
release, validates its manifest, and replaces `manifest.json` last. Previous
release directories and the previous manifest remain available for rollback.
PNG fallback figures are generated from the same captured evidence.

## Initial ET / Helmholtz history (superseded; retained provenance)

`ch05/energy_history` is now the fourth manifest asset. Its `iteration` axis
contains updates 1–12, `frames` has shape [12,32,48], `reference` and `masked`
have shape [32,48], and `energy` / `relative_error` each contain 12 values.
The image view is normalized streamwise velocity at native z-index 16.
Energy covers all tokens in the full 3D input, while the relative-L2 trace
covers the displayed slice. They are not interchangeable metrics.

The original `reconstruction_history` method replays the saved checkpoint and
masked test sample 0 without training. Raw files retain all decoded volumes.
The final update agrees with ordinary inference in the replay runtime; it
differs from the archived output by 0.247% relative L2. The deck and metadata
qualify that difference; its cause has not been established. See the collection
package at `data/raw/ch05/energy_history/` for source hashes and reproduction.

The SNN viewer now derives signed pointwise error from the unchanged prefix
arrays against both reference and ANN. Each error scale is fixed across all
prefixes. Barycentric scalar interpolation on native triangles produces a
seam-free display; error metrics still use original nodes. The static error
fallback is generated by `scripts/prepare_error_fallback.py` in Slurm.

The original four Vue figures are implemented. RFormer physical-time sequences
were subsequently added on slides 31 and 33; see `conditional_views.md`.
To refresh the revised graphics and all verification
after collecting ET, submit `scripts/revise_figures_job.sh`.

## Current requested examples: vortex street and Burgers

The 2026-09-11 additions use `public/data/sequences/` and the generic
`RecordedSequence` player: a straight-reference/saved-optimized trajectory map,
a default 128-agent 2D trajectory with paper-style gray histories, and paired
reference/reconstructed weekly weather maps. Blood playback was subsequently
replaced by the original published static u/v snapshot figures (two 2×2 panels).
These frame indexes carry source and frame hashes; fallbacks are copied from
the identical first frames. See `added_sequences.md` for reproduction and
scientific qualifications. There are now 46 slides; subsequent chapter-7 page
numbers shift by one after the weather/blood split.

Chapter 6 additionally uses local, checksummed PNG time sequences under
`public/data/ch06/time/`, with one JSON index per case. They are rendered from
saved native arrays by `scripts/export_rformer_time.py`; submit
`scripts/rformer_time_job.sh` to regenerate and verify the complete deck.
See `conditional_views.md` for reference recovery, temporal ordering and
spatial interpolation qualifications. No model inference is performed.

The active ET asset is now `vortex_street_2d`, with v-field shape [128,256]
and history shape [12,128,256]. Native pixels are displayed without smoothing.
Reference/reconstruction use fixed reference-range colors, with the percentage
of saturated values reported; stored values and errors are never clipped.
The endpoint differs from archived output by 0.111% relative L2. Its v-field
error changes from 0.84265 to 0.04610. The previous jet release remains archived.

The active chapter-3 asset is `burgers_fresh_prefix`. Its `T` axis contains
every integer 1–128, `frames` has shape [128,201,300], and `reference` has shape
[201,300] in [physical time,space] order. The browser derives signed difference
from the current frame. Frames are hash-checked little-endian float32 binary;
the remaining tensors and binary descriptor are in the versioned JSON asset.
A fresh advanced-CAA calibration at horizon 128 uses the original ANN
checkpoint, verified to match the archived ANN predictions exactly. Weights
and thresholds remain fixed. Raw per-step emissions validate every cumulative
prefix; no fields are interpolated. The archived calibrated state was absent,
so this new run does not claim to reproduce the historical T=64/T=128 pair.
The view has exactly three fields: reference, SNN, signed difference.

The collector corrects the source CSV reference/coordinate ordering mismatch
using the generator's documented array layout and checks sin(x) initial data
and zero boundary values. It preserves original source files and records the
correction. Fresh-prefix relative errors are 0.117553 (T=64), 0.083298 (T=96)
and 0.073741 (T=128). Evaluation remains on the saved training residual grid.
See `data/raw/ch03/burgers_over_t/README.md` for all qualifications.

Collect with `data/raw/ch03/burgers_over_t/replay_job.sh`, publish using
`scripts/export_burgers_prefix.py`, and collect ET with
`data/raw/ch05/energy_history/job.sh` (sequentially, since both update the
manifest), then run `scripts/revise_figures_job.sh`. The legacy
`export_assets_job.sh` exports the old Helmholtz contract and should not be
used to refresh this Burgers view.
