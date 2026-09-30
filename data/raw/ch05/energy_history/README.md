# Energy Transformer reconstruction history

Run `sbatch data/raw/ch05/energy_history/job.sh` from `presentation/`.
The CPU Slurm job reuses pinned historical JAX/Equinox Python 3.11 packages
with the available Python 3.11 runtime. It reads original model code, saved
checkpoint and masked test input; it never trains or modifies the source run.

The current case is the requested **2D vortex street**:
`infer_lr=1e-4_e=10k_mr=0.9_ps=8_hh=2048`, test sample 0. All 12 decoded
128×256×4 states and learned energies are recorded. The browser shows the
native v channel (index 1 in U,V,P,T) without smoothing or image resampling.
The v-field relative L2 changes from 0.84265 to 0.04610.

The replay endpoint agrees with ordinary inference in this runtime. Versus
archived output it differs by 0.001113505 relative L2 (0.111%) and 0.004988223
maximum absolute. The cause is unresolved; the deck retains this qualification.
Metadata records source/checkpoint hashes, dimensions, runtime and Slurm job.

Active capture: `runs/20260910T171240-6195303/`. Earlier 3D-jet captures are
retained as superseded inputs, not used in the active presentation.

After recollecting, run `scripts/revise_figures_job.sh` to validate the raw
and browser data, rebuild, and audit the deck/PDF.
