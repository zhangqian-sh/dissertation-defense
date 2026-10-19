"""Replay the archived fixed-T=64 Poisson conversion; publish measured prefixes.

Run in Slurm. No training, recalibration, synthetic frames, or time interpolation.
Raw arrays and source hashes stay under data/raw; the browser gets one binary.
"""
import os, sys, json, hashlib, subprocess
from pathlib import Path
import numpy as np
import h5py
import torch

ROOT = Path(__file__).resolve().parents[1]
CODE = Path('/users/qzhang64/Projects/SpikingNN/Conversion/SNN-CAACT')
SOURCE = Path('/oscar/data/gk/qzhang64/Projects/SpikingNN/Conversion/SNN-CAACT')
assert os.environ.get('SLURM_JOB_ID'), 'Run through Slurm'
os.environ.update(ACTIVATION='Tanh', CAACT='True')
sys.path.insert(0, str(CODE))
from src.conversion.models.mlp import MLP
from src.conversion.models.spiking_layer import SpikeModel, SpikeModule

torch.set_num_threads(2)
sha = lambda path: hashlib.sha256(Path(path).read_bytes()).hexdigest()
folder = SOURCE/'result/poisson/T=0064/Tanh/advanced_caa'
T = 64
raw = ROOT/'data/raw/ch03/poisson_prefix'/os.environ['SLURM_JOB_ID']
raw.mkdir(parents=True, exist_ok=True)
x = np.loadtxt(folder/'snn_x.csv', delimiter=',').astype(np.float32)
saved = np.loadtxt(folder/'snn_y.csv', delimiter=',').ravel()
ax = np.loadtxt(folder/'ann_x.csv', delimiter=',').astype(np.float32)
av = np.loadtxt(folder/'ann_y.csv', delimiter=',').ravel()
order = np.lexsort((x[:,0], x[:,1])); ann_order = np.lexsort((ax[:,0], ax[:,1]))
x, saved, ax, av = x[order], saved[order], ax[ann_order], av[ann_order]
np.testing.assert_array_equal(x, ax)
space_x, space_y = np.unique(x[:,0]), np.unique(x[:,1])
rows, cols = len(space_y), len(space_x)
assert rows*cols == len(x), 'Archived coordinates must form a full grid'
xx, yy = np.meshgrid(space_x, space_y)
np.testing.assert_array_equal(x, np.stack([xx.ravel(), yy.ravel()], axis=1))

# Find the ANN that actually generated the archived field, rather than assuming
# that the mutable poisson.h5 still points to the historical checkpoint.
ann = MLP([2,100,100,100,1], activation='Tanh', use_bn=False).eval()
probe = np.linspace(0, len(x)-1, min(1024,len(x)), dtype=int)
best = (float('inf'), None)
def load_ann(path):
    with h5py.File(path) as f:
        params = []
        for layer in f['params'].values():
            params.extend([layer['kernel'][()].T, layer['bias'][()]])
    ann.load_state_dict({k:torch.tensor(v) for k,v in zip(ann.state_dict(),params)}, strict=True)
for path in [SOURCE/'saved_model/poisson.h5', *sorted((SOURCE/'saved_model').glob('poisson-seed*.h5'))]:
    load_ann(path)
    with torch.no_grad(): pred = ann(torch.tensor(x[probe])).numpy().ravel()
    error = float(np.linalg.norm(pred-av[probe])/np.linalg.norm(av[probe]))
    print('ANN candidate', path.name, error, flush=True)
    if error < best[0]: best = error, path
assert best[0] < 1e-5, f'No matching ANN checkpoint: {best}'
load_ann(best[1])
with torch.no_grad(): ann_values = ann(torch.tensor(x)).numpy().ravel()
ann_match = float(np.linalg.norm(ann_values-av)/np.linalg.norm(av))
assert ann_match < 1e-5

snn = SpikeModel(MLP([2,100,100,100,1], activation='Tanh', use_bn=False), sim_length=T).eval()
params = torch.load(folder/'snn_converted.pt', map_location='cpu', weights_only=False)
for name, module in snn.named_modules():
    if isinstance(module, SpikeModule):
        for attr in ['threshold_positive', 'threshold_negative']:
            value = params.pop(name+'.'+attr)
            setattr(module, attr, torch.as_tensor(value))
snn.load_state_dict(params, strict=True)
snn.set_spike_state(True)
spikes = np.empty((T, len(x)), dtype=np.float32)
with torch.no_grad():
    for start in range(0,len(x),2048):
        inp = torch.tensor(x[start:start+2048])
        snn.init_membrane_potential()
        for step in range(T):
            spikes[step,start:start+len(inp)] = snn.model(inp).numpy().ravel()
        # Verify explicit stepwise capture against the source model's forward.
        np.testing.assert_allclose(spikes[:,start:start+len(inp)].sum(0)/T,
                                   snn(inp).numpy().ravel(), atol=2e-6, rtol=2e-5)
        print('Captured', start+len(inp), '/', len(x), flush=True)
frames = (np.cumsum(spikes.astype(np.float64), axis=0)/np.arange(1,T+1)[:,None]).astype(np.float32)
match = float(np.linalg.norm(frames[-1]-saved)/np.linalg.norm(saved))
error = np.linalg.norm(frames-av,axis=1)/np.linalg.norm(av)
print('Archived SNN discrepancy:', match, 'final conversion error:', error[-1], flush=True)
assert match < 5e-4, 'Saved SNN replay does not reproduce archived output'
assert np.isfinite(frames).all()
frames = frames.reshape(T,rows,cols)
reference = av.astype(np.float32).reshape(rows,cols)
np.savez_compressed(raw/'payload.npz', frames=frames, step_spikes=spikes.reshape(T,rows,cols),
                    ann_output=reference, archived_snn=saved.reshape(rows,cols),
                    relative_error=error, x=space_x, y=space_y)
inputs = [folder/n for n in ['snn_converted.pt','snn_x.csv','snn_y.csv','ann_x.csv','ann_y.csv']]
inputs += [best[1], CODE/'src/conversion/models/spiking_layer.py', Path(__file__)]
metadata = dict(protocol='Archived calibrated Poisson SNN, fixed T=64; cumulative means of actual emitted output spikes. No recalibration or temporal interpolation.',
                calibration_T=T, rows=rows, cols=cols, ann_checkpoint=str(best[1]),
                ann_relative_discrepancy=ann_match, archived_snn_relative_discrepancy=match,
                final_conversion_error=float(error[-1]), raw_path=str(raw.relative_to(ROOT)),
                input_files=[dict(path=str(p),sha256=sha(p)) for p in inputs],
                torch_version=torch.__version__, units=dict(space='x,y in [-1,1]',T='internal spike steps'))
with np.load(raw/'payload.npz') as arrays:
    shapes = {k:list(arrays[k].shape) for k in arrays.files}
metadata.update(schema_version=2, case_id='poisson', run_id=os.environ['SLURM_JOB_ID'],
    source_repository=str(CODE),
    source_commit=subprocess.check_output(['git','-C',str(CODE),'rev-parse','HEAD'],text=True).strip(),
    source_dirty_state=subprocess.check_output(['git','-C',str(CODE),'status','--short'],text=True),
    configuration_sha256=sha(SOURCE/'config/poisson.yaml'), checkpoint_sha256=sha(folder/'snn_converted.pt'),
    environment=dict(torch=torch.__version__,numpy=np.__version__),
    slurm={k:v for k,v in os.environ.items() if k.startswith('SLURM_')},
    sample_ids=['full archived Poisson evaluation grid'], split='archived PINN evaluation grid',
    normalization='none',shapes=shapes,command='python scripts/export_poisson_prefix.py',
    payload_sha256=sha(raw/'payload.npz'))
(raw/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')

out = ROOT/'public/data/sequences';out.mkdir(parents=True,exist_ok=True)
binary = out/'poisson-prefix.f32';frames.astype('<f4').tofile(binary)
def tensor(values):
    v=np.asarray(values)
    return dict(dtype=str(v.dtype),shape=list(v.shape),order='C',values=v.ravel().tolist())
# Use a shared fixed scale for ANN and SNN; signed difference has its own fixed
# scale across all 64 frames. No autoscaling can mimic improvement.
field_limit = float(max(np.abs(frames).max(),np.abs(reference).max()))
difference_limit = 0.03
payload = dict(benchmark='poisson_archived_prefix', frames=dict(dtype='float32',shape=list(frames.shape),order='C',byte_order='little',
                          binary_path='/data/sequences/poisson-prefix.f32',sha256=sha(binary)),
               reference=tensor(reference), relative_error=tensor(error),T=tensor(np.arange(1,T+1)),
               field_limit=field_limit,field_min=0.0,field_max=0.32,difference_limit=difference_limit,metadata=metadata)
asset = out/'poisson-prefix.json'
state = 'poisson-archived-fixed64-prefix'
envelope = dict(schema_version=2,asset_id='ch03/poisson_prefix',chapter='ch03',units=metadata['units'],
                defaults=dict(state_id=state),
                source=dict(thesis_refs=['fig:conversion:poisson'],raw_collection_path=str(raw.relative_to(ROOT)),
                            raw_sha256=sha(raw/'payload.npz'),metadata_sha256=sha(raw/'metadata.json')),
                data=dict(states=[dict(id=state,case_id='poisson',run_id=os.environ['SLURM_JOB_ID'],
                                      status='tested',protocol_id='archived-fixed64-prefix',payload=payload)]))
asset.write_text(json.dumps(envelope,separators=(',',':'))+'\n')

# The live renderer and PDF fallback use the same fixed color scales.
from restyle_poisson_prefix import render_fallback
fallback = render_fallback(ROOT, payload, frames)
manifest_path=ROOT/'public/data/manifest.json'
manifest=json.loads(manifest_path.read_text())
manifest['assets']=[a for a in manifest['assets'] if a['asset_id']!='ch03/poisson_prefix']
manifest['assets'].append(dict(asset_id='ch03/poisson_prefix',chapter='ch03',component='PoissonSpikeDynamics',
        path='sequences/poisson-prefix.json',default_state=state,fallback_path='/fallback_figures/ch03/poisson_prefix.png',
        sha256=sha(asset),fallback_sha256=sha(fallback),status='required'))
manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
print('Published',binary.stat().st_size,'bytes;',rows,'x',cols,'x',T,'frames',flush=True)
