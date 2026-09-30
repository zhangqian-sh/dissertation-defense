# Burgers reference / SNN / difference across T

## Active intermediate-field capture

Run `replay_job.sh` through Slurm from the presentation directory. `replay.py`
loads `saved_model/burgers.h5`, whose full-grid ANN predictions exactly match
the archived ANN, and performs fresh advanced-CAA calibration at horizon 128.
Seed 0 selects 8192 calibration nodes; the original calibration routine uses
5000 optimization iterations per layer. Source checkpoints remain read-only.
The resulting weights, thresholds and horizon stay fixed while recording every
emitted spike step on all 201×300 nodes. Every field T=1–128 is its actual
cumulative output mean, not interpolation or a separately calibrated model.
Early silent prefixes can be identical. Prefix length is not physical time.

Active run: `runs/20260910T173037-prefix-6195542/` (GPU job 6195542).
Raw arrays retain per-step emissions, all prefix fields, reference and errors;
metadata records hashes, calibration protocol and checkpoint provenance.
The final prefix is checked against ordinary 128-step inference. Relative L2
errors at T=64,96,128 are 0.117553, 0.083298 and 0.073741. This is a new
calibration, not reproduction of the unavailable archived calibrated state.

Publish with `scripts/export_burgers_prefix.py --raw <run-directory>` on Slurm,
then run `scripts/revise_figures_job.sh`. The browser loads hash-checked
little-endian float32 fields and derives the current signed difference. Both
color scales remain fixed across all prefixes. The alignment correction and
training-grid evaluation limitation described below still apply.

## Historical archived pair

Submit `job.sh` from the presentation directory. It captures the matched
archived seed-0 advanced-CAA runs at **T=64 and T=128**. Both have exactly equal
ANN predictions on the full 201×300 space-time grid. Other available T runs
use different ANN predictions, so they are not mixed into this comparison.
No intermediate T fields are interpolated or synthesized. These are per-T
calibrated runs, not prefixes of a fixed-calibration SNN.

The source `generate_burgers_data` flattens its solution in [time,space] order,
but flattens `meshgrid(time,space)` in [space,time] order. Consequently, the
archived CSV reference values are not correctly paired with the coordinate
rows. The collector restores the native 201×300 reference layout, orders SNN
predictions by actual coordinates, and verifies the sine initial condition,
zero boundaries, common reference, and matched ANN. Source files are read-only.
Corrected relative errors are 0.128166 at T=64 and 0.073256 at T=128.

The view covers x∈[0,2π], physical t∈[0,4], ν=0.01. The displayed difference is
SNN−reference. Reference/SNN share one fixed color scale, and difference has
a separate scale fixed across T. This uses the saved training residual grid,
not a held-out generalization experiment. Calibration/checkpoint reproduction
is not claimed: only archived predictions are collected with input hashes.

Historical run: `runs/20260910T171508-6195332/`. `metadata.json` records source
files, hashes, alignment qualification, protocol, environment and Slurm job.
Recollection publishes a new immutable raw capture and browser release.
