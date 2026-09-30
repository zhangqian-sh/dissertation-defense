# drone_swarm_3d raw collection

Run from the presentation directory:

```bash
mkdir -p data/raw/ch07/drone_swarm_3d/logs
sbatch data/raw/ch07/drone_swarm_3d/job.sh
```

The JSON-formatted YAML run index records the selected saved experiment.
The collector accepts `--case-id`, `--run-id`, `--source-root` and
`--code-root`; the last two allow relocation of the source project trees.
The launcher explicitly uses the existing OCFormer environment for NumPy,
h5py and YAML only. No model is loaded, trained, or changed.

Each run writes `runs/ball_3d_M16/saved_lbfgs/{metadata.json,payload.npz}`.
Existing runs are never overwritten. Metadata is written after the payload;
only then is the complete directory published. Incomplete directories use a
`.partial-JOBID` suffix and are never exporter inputs. Source files remain
read-only. Metadata includes checksums, audited source commit/dirty state,
protocol, units, sample identity and Slurm allocation; historical training
commits are unknown and explicitly distinguished from current source identity.

Derived arrays and browser payloads are generated separately by
`scripts/export_defense_assets.py`. See the metadata for scientific
qualifications. This package reuses saved outputs and does not claim to have
reproduced the original training environment.
