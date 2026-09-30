# Conditional interaction decisions

## Energy Transformer

Playback is now enabled on slide 20. The initial deck had no saved iteration
sequence and omitted this view. Further source inspection found the original
`reconstruction_history` method and saved checkpoints with their masked
test inputs. The collector now replays saved sample 0 for 12 actual token
updates (step size 0.1), decoding each update without training or synthetic
interpolation in iteration time. The current browser view uses the requested
2D vortex-street case: native 128×256 cross-stream velocity (v), with playback,
scrubbing, wheel stepping, a signed-error toggle, and linked v-field-error /
full-system-energy traces. The earlier 3D-jet view is superseded. Canvas pixels
are native-resolution and display smoothing is disabled, preserving detail.

This is explicitly a new checkpoint replay, not an exact historical-runtime
reproduction. The endpoint agrees with ordinary inference in the replay
runtime; versus the archived prediction it differs by 0.111% relative L2
(maximum absolute discrepancy 0.00498822). The cause of that discrepancy has
not been established. Both discrepancy measures and source/checkpoint hashes
are retained in raw metadata. The selected v-field's relative L2 changes from
0.84265 to 0.04610; no monotonic-energy guarantee is asserted.

`data/raw/ch05/energy_history/collect.py` and its Slurm launcher reproduce this
capture. Masked input has its own labeled color scale; reference/reconstruction
share the fixed reference min/max range across updates. This avoids early
outliers washing out final flow structure. Values outside this color range
saturate, and the current percentage is shown explicitly. Signed error has
its own fixed scale. No values or metrics are clipped, and no spatial display
interpolation or temporal frame synthesis is used.

## RFormer

Physical-time playback is explicitly requested and enabled on CH6–27 and
CH6–29. `RFormerTime.vue` displays synchronized reference, observations and
RFormer, with play/pause, reset and frame seeking. CH6–27 has u, v, p rows in
a 3×3 matrix; CH6–29 has three vector-field panels. All frames use
fixed component color scales or a fixed arrow scale. Leaving a slide pauses its playback; printing uses a
static first-frame fallback. The published baseline spectrum stays static and
is labeled as unrelated to the currently selected frame.

`scripts/export_rformer_time.py` reads saved RFormer predictions (no inference
or training). The vortex case contains 20 successive test snapshots, source
times 80–99, displaying u/v/p and the original 512-observation protocol.
The jet case contains 40 shuffled test snapshots: matching observed coordinates
and velocities to raw tracks recovers their physical-time indices, then frames
are sorted. These indices are not seconds; gaps are not interpolated and
playback advances one saved snapshot at a time. Its test qv is intentionally
zero-filled; reference comes from paired validation data after exact checks of
coordinates and observed values. The result directory named `case4` actually
contains the jet run, verified from its config; `case3` contains blood flow.

Reconstructed full fields retain measured observation
values and use predicted query values; unused observation-token outputs are
discarded as specified by the source protocol. Vortex full fields are linearly
interpolated with the cylinder interior masked; observation panels show only
the measured, colored points without filling the gaps. Each component shares
one fixed symmetric scale across all three columns and all physical times.
Jet native points in |z| < 5 are projected to x–y; arrows show the actual (u,v)
components, without spatial interpolation or vector normalization. The original
view bounds x∈[-15,15], y∈[-30,40] are retained. Reference and RFormer use the
same deterministic subset of at most 900 points per frame; observations use
all observed points within the slab/view. Arrow scale is fixed at 0.08 with
a 0.2 velocity key, across all panels and times. This is a projected slab, not
an exact plane or full 3D vector display. The exported PNG sequences include source/reference
hashes, original row order, times, frame checksums and Slurm job in JSON.
Browser loading verifies frame hashes. No temporal frames are synthesized.
Published aggregate errors remain qualified as published all-component results,
not errors computed from the current rasterized component.

Rotation and movable 3D slicing remain disabled. Weather and blood have
separate slides (30 and 31): paired dynamic weather maps and original static
u/v blood snapshots, preserving dataset-specific qualifications.
See `added_sequences.md` for their source alignment, spatial processing and
time labels, as well as the new OCFormer illustration and 128-agent example.
