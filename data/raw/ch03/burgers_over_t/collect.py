"""Capture matched saved Burgers T=64/128 runs, with audited grid alignment."""
import hashlib,json,os,subprocess,shutil
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[4]
SOURCE=Path('/oscar/data/gk/qzhang64/Projects/SpikingNN/Conversion/SNN-CAACT')
CODE=Path('/users/qzhang64/Projects/SpikingNN/Conversion/SNN-CAACT')
assert os.environ.get('SLURM_JOB_ID')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def tensor(v):
    v=np.asarray(v);assert np.isfinite(v).all()
    return dict(dtype=str(v.dtype),shape=list(v.shape),order='C',values=v.ravel().tolist())
T=np.array([64,128],dtype=np.int32); predictions=[];inputs=[];ann_previous=None;reference=None
for t in T:
    path=SOURCE/f'bak/result/burgers-seed0/T={t:04d}/Tanh/advanced_caa'
    arrays={name:np.loadtxt(path/(name+'.csv'),delimiter=',') for name in ['snn_x','snn_y','snn_y_true','ann_x','ann_y','ann_y_true']}
    inputs.extend(dict(path=str(path/(name+'.csv')),sha256=sha(path/(name+'.csv'))) for name in arrays)
    x=arrays['snn_x'];time=np.unique(x[:,0]);space=np.unique(x[:,1]);assert (len(time),len(space))==(201,300)
    # The source generator flattens u[t,x] but meshgrid(t,x) in x-major order.
    # CSV y_true is therefore NOT paired to CSV x. Restore the documented native
    # [time,space] layout rather than using the mismatched CSV row association.
    np.testing.assert_allclose(x[:,0].reshape(300,201),np.broadcast_to(time,(300,201)))
    np.testing.assert_allclose(x[:,1].reshape(300,201),np.broadcast_to(space[:,None],(300,201)))
    ref=arrays['snn_y_true'].reshape(201,300)
    np.testing.assert_allclose(ref[0],np.sin(space),atol=3e-7)
    np.testing.assert_allclose(ref[:,[0,-1]],0,atol=1e-7)
    idx=np.lexsort((x[:,1],x[:,0])); ax=arrays['ann_x'];ai=np.lexsort((ax[:,1],ax[:,0]))
    np.testing.assert_array_equal(x[idx],ax[ai])
    ann=arrays['ann_y'][ai].reshape(201,300)
    if reference is not None:
        np.testing.assert_array_equal(reference,ref)
        np.testing.assert_array_equal(ann_previous,ann)
    reference=ref;ann_previous=ann;predictions.append(arrays['snn_y'][idx].reshape(201,300))
frames=np.stack(predictions);difference=frames-reference
relative=np.linalg.norm(difference.reshape(len(T),-1),axis=1)/np.linalg.norm(reference)
print('Burgers reference alignment verified; relative errors:',relative,flush=True)
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')+'-'+os.environ['SLURM_JOB_ID']
raw=Path(__file__).parent/'runs'/stamp;raw.mkdir(parents=True)
raw_arrays=dict(T=T,reference=reference,frames=frames,difference=difference,relative_error=relative,time=time,space=space,ann_output=ann_previous)
np.savez_compressed(raw/'payload.npz',**raw_arrays)
meta=dict(schema_version=2,case_id='burgers_seed0',run_id=stamp,source_repository=str(CODE),
 source_commit=subprocess.check_output(['git','-C',str(CODE),'rev-parse','HEAD'],text=True).strip(),
 source_dirty_state=subprocess.check_output(['git','-C',str(CODE),'status','--short'],text=True),
 configuration_sha256=sha(SOURCE/'config/burgers.yaml'),checkpoint_sha256=None,
 environment=dict(numpy=np.__version__),slurm={k:v for k,v in os.environ.items() if k.startswith('SLURM_')},
 sample_ids=['entire saved 201x300 grid'],split='saved PINN evaluation on training residual grid; not a held-out generalization claim',
 normalization='none',units=dict(field='u, benchmark units',space='x in [0,2π]',time='physical t in [0,4]',T='SNN simulation length'),
 shapes={k:list(v.shape) for k,v in raw_arrays.items()},command='python data/raw/ch03/burgers_over_t/collect.py',
 payload_sha256=sha(raw/'payload.npz'),input_files=inputs,
 protocol='Two independently calibrated saved advanced-CAA Tanh runs, same seed0 ANN predictions verified exactly. T is not an internal prefix of one fixed calibration.',
 reference_alignment='Source generate_burgers_data flattens solution [201,300] in time-major order while coordinates are space-major. Corrected reference layout from native dimensions; initial sin(x) and zero boundaries checked.',
 generator_sha256=sha(CODE/'example/dataset/burgers.py'))
(raw/'metadata.json').write_text(json.dumps(meta,indent=2)+'\n')
payload={k:tensor(v) for k,v in raw_arrays.items()};payload.update(benchmark='burgers_1d_spacetime',metadata=meta)
release=ROOT/'public/data/releases'/stamp/'ch03';release.mkdir(parents=True)
asset=release/'conversion_over_t.json';state='burgers-seed0-saved-T64-T128'
envelope=dict(schema_version=2,asset_id='ch03/conversion_over_t',chapter='ch03',units=meta['units'],defaults=dict(state_id=state),
 source=dict(thesis_refs=['ch:conversion-hardware'],raw_collection_path=str(raw.relative_to(ROOT)),raw_sha256=sha(raw/'payload.npz'),metadata_sha256=sha(raw/'metadata.json')),
 data=dict(states=[dict(id=state,case_id=meta['case_id'],run_id=stamp,status='exploratory',protocol_id='saved-matched-T-sweep',payload=payload)]))
asset.write_text(json.dumps(envelope,separators=(',',':'))+'\n')
fig,axes=plt.subplots(1,3,figsize=(12,3.8),layout='constrained');limit=max(np.abs(reference).max(),np.abs(frames).max());elimit=np.abs(difference).max()
for ax,v,title,l in zip(axes,[reference,frames[0],difference[0]],['Reference','SNN · T=64','SNN − reference'],[limit,limit,elimit]):
    im=ax.imshow(v,origin='lower',extent=[space[0],space[-1],time[0],time[-1]],aspect='auto',interpolation='nearest',cmap='RdBu_r',vmin=-l,vmax=l)
    ax.set(title=title,xlabel='x',ylabel='physical t');fig.colorbar(im,ax=ax,shrink=.8)
png=release/'conversion_over_t.png';fig.savefig(png,dpi=180);plt.close(fig)
shutil.copyfile(png,ROOT/'public/fallback_figures/ch03/conversion_over_t.png')
mp=ROOT/'public/data/manifest.json';m=json.loads(mp.read_text());m['assets']=[a for a in m['assets'] if a['asset_id']!='ch03/conversion_over_t']
m['assets'].append(dict(asset_id='ch03/conversion_over_t',chapter='ch03',component='ConversionOverT',path=str(asset.relative_to(mp.parent)),default_state=state,fallback_path='/'+str(png.relative_to(ROOT/'public')),sha256=sha(asset),fallback_sha256=sha(png),status='required'))
m['generated_at']=datetime.now(timezone.utc).isoformat();mp.write_text(json.dumps(m,indent=2)+'\n')
print('Published',asset,flush=True)
