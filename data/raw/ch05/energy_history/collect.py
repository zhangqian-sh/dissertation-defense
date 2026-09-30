"""Replay one saved ET test input; never train or alter the source experiment."""
import hashlib
import json
import os
from pathlib import Path
import sys
import subprocess
from datetime import datetime, timezone

import equinox as eqx
import h5py
import jax
import jax.numpy as jnp
import numpy as np
from einops import rearrange
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[4]
CODE = Path('/users/qzhang64/Projects/OperatorLearning/ETRO/examples/vortex_street')
SOURCE = Path('/oscar/data/gk/qzhang64/Projects/OperatorLearning/ETRO/vortex_street/results/infer_lr=1e-4_e=10k_mr=0.9_ps=8_hh=2048')
sys.path.insert(0, str(CODE))
from model import ReconstructionOperator, generate_positional_encoding_2d

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()

def tensor(a):
    a = np.asarray(a)
    assert np.isfinite(a).all()
    return dict(dtype=str(a.dtype), shape=list(a.shape), order='C', values=a.ravel().tolist())

assert os.environ.get('SLURM_JOB_ID'), 'Run on a compute node'
with h5py.File(SOURCE/'output/test.h5', 'r') as f:
    print({k: f[k].shape for k in f}, flush=True)
    original, masked, saved = [f[k][0] for k in ('original', 'masked', 'reconstructed')]
assert original.shape == (128,256,4)
model = ReconstructionOperator(
    config_embedder=dict(patch_dim=8**2*4, token_dim=256, values_dim=4),
    config_energy_transformer=dict(num_heads=8, hopfield_type='softmax', hopfield_hidden_dim=2048),
    positional_embedding=generate_positional_encoding_2d(16,32,256).astype(np.float32),
    key=jax.random.PRNGKey(2024))
model = eqx.tree_deserialise_leaves(SOURCE/'model/test.eqx', model)
patches = rearrange(masked, '(x a) (y b) d -> (x y) (d a b)', a=8,b=8)
@eqx.filter_jit
def replay(m, x):
    return m.reconstruction_history(x, n_iters=12, alpha=0.1)
final, energies, history = replay(model, jnp.asarray(patches))
history = rearrange(np.asarray(history), 't (x y) (d a b) -> t (x a) (y b) d', x=16,y=32,a=8,b=8,d=4)
final = rearrange(np.asarray(final), '(x y) (d a b) -> (x a) (y b) d', x=16,y=32,a=8,b=8,d=4)
np.testing.assert_allclose(history[-1], final, atol=1e-7, rtol=1e-6)
max_difference = float(np.max(np.abs(final-saved)))
relative_difference = float(np.linalg.norm(final-saved)/np.linalg.norm(saved))
ordinary = eqx.filter_jit(lambda m,x:m(x,n_iters=12,alpha=0.1))(model,jnp.asarray(patches))
ordinary = rearrange(np.asarray(ordinary), '(x y) (d a b) -> (x a) (y b) d', x=16,y=32,a=8,b=8,d=4)
np.testing.assert_allclose(final,ordinary,atol=2e-6,rtol=2e-5)
print('Archived final discrepancy: max',max_difference,'relative L2',relative_difference,flush=True)
# This is a new checkpoint replay, not a bitwise reconstruction of the old GPU
# runtime. Fail on a material mismatch; retain the measured discrepancy.
assert relative_difference < .01 and max_difference < .01*np.max(np.abs(saved))
stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')+'-'+os.environ['SLURM_JOB_ID']
raw = Path(__file__).parent/'runs'/stamp
raw.mkdir(parents=True, exist_ok=False)
raw_arrays=dict(original=original, masked_volume=masked, history=history, energy=np.asarray(energies))
np.savez_compressed(raw/'payload.npz', **raw_arrays)
metadata = dict(sample_index=0, source_run=str(SOURCE), source_code=str(CODE/'model.py'),
    checkpoint_sha256=sha(SOURCE/'model/test.eqx'), input_sha256=sha(SOURCE/'output/test.h5'),
    source_code_sha256=sha(CODE/'model.py'), collector_sha256=sha(__file__),
    n_iters=12, alpha=0.1, patch_size=8, nominal_mask_rate=0.9,
    final_max_abs_difference_from_saved=max_difference, final_relative_l2_difference_from_saved=relative_difference,
    archived_output_exactly_reproduced=False, job_id=os.environ['SLURM_JOB_ID'],
    versions=dict(jax=jax.__version__, equinox=eqx.__version__, numpy=np.__version__),
    protocol='Fresh deterministic inference replay of saved masked test sample 0; no retraining. Each frame is decoded after an actual token update. No synthetic intermediate frames.',
    view='2D vortex street, v component (U,V,P,T channel index 1), native 128x256 grid. Error covers the v field; energy covers the full token system.')
metadata.update(schema_version=2,case_id='vortex2d_sample0',run_id=stamp,
    source_repository=str(CODE.parents[1]),source_commit=subprocess.check_output(['git','-C',str(CODE),'rev-parse','HEAD'],text=True).strip(),
    source_dirty_state=subprocess.check_output(['git','-C',str(CODE),'status','--short'],text=True),
    configuration_sha256=sha(CODE/'config.yaml'),environment=metadata['versions'],
    slurm={k:v for k,v in os.environ.items() if k.startswith('SLURM_')},sample_ids=[0],split='saved test',
    normalization='Saved normalized velocity and pressure; no new normalization',units=dict(field='source normalized velocity',iteration='token update',energy='learned energy'),
    shapes={k:list(v.shape) for k,v in raw_arrays.items()},command='python3.11 data/raw/ch05/energy_history/collect.py',
    payload_sha256=sha(raw/'payload.npz'),input_files=[dict(path=str(SOURCE/'output/test.h5'),sha256=metadata['input_sha256']),dict(path=str(SOURCE/'model/test.eqx'),sha256=metadata['checkpoint_sha256'])])
(raw/'metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
reference=original[:,:,1]; observed=masked[:,:,1]; frames=history[:,:,:,1]
relative=np.linalg.norm((frames-reference).reshape(12,-1),axis=1)/np.linalg.norm(reference)
payload=dict(benchmark='vortex_street_2d',component='v',iteration=tensor(np.arange(1,13,dtype=np.int32)), reference=tensor(reference),
    masked=tensor(observed), frames=tensor(frames), energy=tensor(np.asarray(energies)),
    relative_error=tensor(relative), metadata=metadata)
release=ROOT/'public/data/releases'/stamp/'ch05'; release.mkdir(parents=True)
asset=release/'energy_history.json'
envelope=dict(schema_version=2,asset_id='ch05/energy_history',chapter='ch05',
    defaults=dict(state_id='vortex2d-sample0-v'),source=dict(thesis_refs=['fig:et:architecture','eq:et:update'],raw_collection_path=str(raw.relative_to(ROOT)),raw_sha256=sha(raw/'payload.npz'),metadata_sha256=sha(raw/'metadata.json')),
    units=dict(field='source normalized velocity',iteration='token update',energy='learned energy'),
    data=dict(states=[dict(id='vortex2d-sample0-v',case_id='vortex2d_sample0',run_id=stamp,status='exploratory',protocol_id='saved-checkpoint-replay-12',payload=payload)]))
asset.write_text(json.dumps(envelope,separators=(',',':'))+'\n')
fig,axes=plt.subplots(1,4,figsize=(13,3.1),layout='constrained')
limit=float(max(np.abs(reference).max(),np.abs(frames).max()))
for ax,v,title in zip(axes,[reference,frames[0],frames[5],frames[-1]],['Reference','Update 1','Update 6','Update 12']):
    im=ax.imshow(v,origin='lower',cmap='RdBu_r',vmin=-limit,vmax=limit,interpolation='nearest'); ax.set_title(title); ax.set_xlabel('column index')
axes[0].set_ylabel('row index');fig.colorbar(im,ax=axes,shrink=.8,label='normalized v')
fallback=release/'energy_history.png';fig.savefig(fallback,dpi=160);plt.close(fig)
import shutil
standalone=ROOT/'public/fallback_figures/ch05/energy_history.png';standalone.parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(fallback,standalone)
manifest_path=ROOT/'public/data/manifest.json';manifest=json.loads(manifest_path.read_text())
manifest['assets']=[a for a in manifest['assets'] if a['asset_id']!='ch05/energy_history']
manifest['assets'].append(dict(asset_id='ch05/energy_history',chapter='ch05',component='EnergyHistory',
    path=str(asset.relative_to(ROOT/'public/data')),default_state='vortex2d-sample0-v',
    fallback_path='/'+str(fallback.relative_to(ROOT/'public')),sha256=sha(asset),fallback_sha256=sha(fallback),status='required'))
manifest['generated_at']=datetime.now(timezone.utc).isoformat()
manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
print('Published',asset,'slice relative errors',relative,flush=True)
