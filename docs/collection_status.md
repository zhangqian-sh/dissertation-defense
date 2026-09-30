# Initial plot-source collection

**Update:** The three required interactive datasets have since been collected
and exported to `public/data/manifest.json`. See [interactive_data.md](interactive_data.md)
for the ready-to-use payloads, reproduction commands and scientific qualifications.
The text below records the initial audit, not the current dynamic collection state.

Collected on 2026-09-09 using `python scripts/collect_thesis_sources.py`.

`data_inventory.csv` contains 102 candidate static thesis figures/tables and
three required dynamic entries. Candidate means source coverage, not a final
slide assignment. Each static record has the original LaTeX block and source
checksums under `figure_sources/`. The 66 PNG/JPEG/SVG inputs have been copied
byte-for-byte to `public/figures/`. PDF inputs remain at their recorded thesis
paths and need browser conversion. Scientific qualifications are retained in
the source blocks; visual readability and chapter-level protocol review remain
pending. No plots were digitized and no model measurements were invented.

Three numeric CSVs were transcribed from their adjacent `source.tex` tables:

- Chapter 2 encoding: relative discrete L2 errors over 200 held-out Poisson
  samples, after Savitzky–Golay smoothing (window 51, polynomial order 3).
  Standard deviation is across samples, not a standard error. K is the spike
  simulation horizon; these are operator prediction errors, not codec errors.
- Appendix B ET temporal: separate trained configurations using fractions of
  the 80-snapshot training sequence, with unchanged mask/architecture. These
  are test relative errors; no uncertainties are supplied in this table.
- Appendix B ET module: 3D jet relative errors. Full ET does not minimize every
  field error. Retain the spectrum comparisons when interpreting these values.

## Dynamic source audit

All 12 candidate locations in the locator exist. Home and data paths resolve
to distinct directories; they must not be treated as interchangeable checkouts.
The following code HEADs were observed, solely for locating sources:

| Code root under `/oscar/home/qzhang64/Projects/` | HEAD |
|---|---|
| `SpikingNN/UNO` | `5d6a2bf8e9f9210655a53800b9263b59ad877703` |
| `SpikingNN/spiking_marching_scheme` | `9868538021915bec47cfd7037b3b50876edf1744` |
| `OptimalControl/OCFormer` | `76df57f14da09c84af8b84020e8386b5c1b3edc7` |

The corresponding data roots did not return Git identities. No inference has
used these commits; dirty states, training commits and checkpoint/config hashes
must be recorded when selecting an actual capture.

- SMS: `SpikingNN/Spiking-Marching-Scheme/results/` under the data project root
  contains `output_data/{train,test}/u_true.csv`, `u_pred.csv`, and
  `u_pred_cascade.csv`, including wave and heat cases. Saved predictions make
  reuse promising. Select a thesis-matched case and verify timestamps,
  normalization, training boundary and encoding configuration before capture.
  The inventory's Van der Pol label is a candidate, not a selected run.
- Conversion: the UNO data root has conversion data and
  `report/20260603/pod_lscale_trace_stats.csv` plus branch trace images. These
  do not establish that emitted per-step output arrays are saved. Inspect the
  final `SpikeModule` capture implementation and saved artifacts before deciding
  whether a new forward pass is needed. Membrane traces cannot replace spikes.
- OCFormer: the data root contains `data/ball_3d/n=16/boundary.h5`,
  `data/ball_3d/n=128/boundary.h5`, `data/room_3d/n=100/boundary.h5`, and saved
  prediction HDF5 files in results. Boundary data alone is insufficient for
  playback. Locate a matching 3D prediction/config and recover original
  constraints and evaluation times before calculating clearance events.

ET playback and RFormer spatial inspection remain undecided: this pass retained
their static evidence but did not inspect native sequences or geometry. They
are not enabled dynamic dependencies. Loihi normalization and original hardware
logs also remain to be audited; the thesis figures/tables are retained without
relabeling their error metrics.

## Next collection pass

Select and verify one saved SMS run and one 3D OCFormer run. Implement their
per-plot collectors and Slurm wrappers against the actual saved formats; inspect
conversion spike capture next. Follow the documented immutable run contract,
and use Slurm for inference or large processing. Explicit payload/log ignore
rules are already installed. No jobs or training were launched in this pass.

The collector refuses conflicting output contents and refuses to replace an
existing inventory, preserving subsequent manual annotations. Run it in a fresh
presentation workspace to reproduce the initial snapshot. The three manually
transcribed CSVs are retained separately from the extraction script.
