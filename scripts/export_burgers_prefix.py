"""Publish a validated raw prefix capture with full-resolution binary frames."""
from pathlib import Path
import os,json,hashlib,shutil,argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1];assert os.environ.get('SLURM_JOB_ID')
parser=argparse.ArgumentParser();parser.add_argument('--raw',type=Path);args=parser.parse_args()
raw=args.raw or sorted((root/'data/raw/ch03/burgers_over_t/runs').glob('*-prefix-*/metadata.json'))[-1].parent
raw=raw.resolve()
meta=json.loads((raw/'metadata.json').read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
assert sha(raw/'payload.npz')==meta['payload_sha256']
with np.load(raw/'payload.npz') as z:a={k:z[k] for k in z.files}
frames=a['frames'];ref=a['reference'];difference=frames-ref
np.testing.assert_allclose(frames,np.cumsum(a['step_spikes'].astype(float),axis=0)/np.arange(1,129)[:,None,None],rtol=2e-6,atol=2e-7)
def tensor(v):
    v=np.asarray(v);assert np.isfinite(v).all()
    return dict(dtype=str(v.dtype),shape=list(v.shape),order='C',values=v.ravel().tolist())
release=root/'public/data/releases'/meta['run_id']/'ch03';release.mkdir(parents=True,exist_ok=False)
binary=release/'burgers-prefix.f32';frames.astype('<f4').tofile(binary)
payload={k:tensor(a[k]) for k in ['T','reference','relative_error','space','time','ann_output']}
payload.update(benchmark='burgers_fresh_prefix',metadata=meta,
    frames=dict(dtype='float32',shape=list(frames.shape),order='C',byte_order='little',binary_path='/'+str(binary.relative_to(root/'public')),sha256=sha(binary)),
    field_limit=float(max(np.abs(frames).max(),np.abs(ref).max())),difference_limit=float(np.abs(difference).max()))
state='burgers-fresh-fixed128-prefix';asset=release/'conversion_over_t.json'
e=dict(schema_version=2,asset_id='ch03/conversion_over_t',chapter='ch03',units=meta['units'],defaults=dict(state_id=state),
 source=dict(thesis_refs=['ch:conversion-hardware'],raw_collection_path=str(raw.relative_to(root)),raw_sha256=sha(raw/'payload.npz'),metadata_sha256=sha(raw/'metadata.json')),
 data=dict(states=[dict(id=state,case_id=meta['case_id'],run_id=meta['run_id'],status='exploratory',protocol_id='fresh-fixed128-cumulative-emission',payload=payload)]))
asset.write_text(json.dumps(e,separators=(',',':'))+'\n')
fig,axes=plt.subplots(1,3,figsize=(12,3.8),layout='constrained')
for ax,v,title,limit in zip(axes,[ref,frames[63],difference[63]],['Reference','SNN · prefix 64 / 128','SNN − reference'],[payload['field_limit'],payload['field_limit'],payload['difference_limit']]):
    im=ax.imshow(v,origin='lower',extent=[0,2*np.pi,0,4],aspect='auto',interpolation='nearest',cmap='RdBu_r',vmin=-limit,vmax=limit)
    ax.set(title=title,xlabel='x',ylabel='physical t');fig.colorbar(im,ax=ax,shrink=.8)
png=release/'conversion_over_t.png';fig.savefig(png,dpi=180);plt.close(fig)
mp=root/'public/data/manifest.json';m=json.loads(mp.read_text());m['assets']=[a for a in m['assets'] if a['asset_id']!='ch03/conversion_over_t']
m['assets'].append(dict(asset_id='ch03/conversion_over_t',chapter='ch03',component='ConversionOverT',path=str(asset.relative_to(mp.parent)),default_state=state,fallback_path='/'+str(png.relative_to(root/'public')),sha256=sha(asset),fallback_sha256=sha(png),status='required'))
pending=mp.with_name('manifest.prefix.pending.json');pending.write_text(json.dumps(m,indent=2)+'\n')
from validate_defense_assets import validate_manifest
validate_manifest(pending)
shutil.copyfile(png,root/'public/fallback_figures/ch03/conversion_over_t.png')
pending.replace(mp)
print('Published 128 genuine Burgers fields:',asset,'binary bytes',binary.stat().st_size,flush=True)
