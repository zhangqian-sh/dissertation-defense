"""Export only the published z-index 16 slice of the 40 saved ET jet test frames.

This lightweight slice extraction performs no training, inference, or smoothing.
"""
from pathlib import Path
import hashlib, json
import h5py
import numpy as np
from matplotlib import colormaps

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/oscar/data/gk/qzhang64/Projects/OperatorLearning/ETRO/jet_3d/results/random-32/random_model_key=2_lr=1e-4_e=10k_run=-1_mr=0.8_ps=8_hh=2048_a6000-seed=2024/output/test.h5")
DEST = ROOT / "public/data/ch05/jet-test"
DEST.mkdir(parents=True, exist_ok=True)
columns = ["original", "masked", "reconstructed"]
with h5py.File(SOURCE) as f:
    # Source channels u,v,w,p; display u,v,p. Match the published imshow orientation.
    frames = np.stack([f[key][:, :, :, 16, :][..., [0, 1, 3]].transpose(0, 3, 1, 2) for key in columns], axis=2).astype("<f4")
assert frames.shape == (40, 3, 3, 32, 48) and np.isfinite(frames).all()
blob = frames.tobytes()
(DEST / "frames.bin").write_bytes(blob)
metadata = dict(shape=list(frames.shape), dtype="float32", byte_order="little", columns=columns,
    channels=["u", "v", "p"], snapshot_indices=list(range(160, 200)), z_index=16,
    orientation="native source slice: first spatial index is the plot row, second is the plot column; row zero at top, matching published panels",
    source=str(SOURCE), source_shape=[40,32,48,32,4], frame_interval_ms=150,
    limits=[[float(frames[:, c, 0].min()), float(frames[:, c, 0].max())] for c in range(3)],
    palette=(colormaps["jet"](np.linspace(0,1,256))[:, :3]*255).round().astype(int).tolist(),
    sha256=hashlib.sha256(blob).hexdigest())
(DEST / "index.json").write_text(json.dumps(metadata, indent=2)+"\n")
print(f"Exported {frames.shape[0]} synchronized test frames: {len(blob):,} bytes")
