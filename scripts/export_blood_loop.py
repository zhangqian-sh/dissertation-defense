"""Export the matched 20-snapshot blood sequence as eight synchronized panels (Slurm CPU only).

Source: prev/results/case3_blood/dpd-averaged/analysis_publication.ipynb.
Same snapshot 5, averaged snapshot 85, |z|<1 plane, and shared 99th-percentile
symmetric color limits per component. Native slide text supplies axes and labels.
"""
from animation_bundle import publish
import os,json,hashlib,shutil,fcntl
from pathlib import Path
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator
import numpy as np
import h5py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
assert os.environ.get('SLURM_JOB_ID'),'Use Slurm'
ROOT=Path(__file__).resolve().parents[1]
RF=Path('/oscar/data/gk/qzhang64/Projects/OperatorLearning/RFormer/prev')
raw=RF/'results/case3_blood/dpd-averaged/obs_10k_q_290k_epoch=10/val.h5'
averaged=RF/'data/blood/raw/averaged/xq_all.h5'
out=ROOT/'data/staging'/f'blood-loop-{os.environ["SLURM_JOB_ID"]}';out.mkdir(parents=True,exist_ok=True)
fixed=json.loads((ROOT/'public/data/ch06/blood-redraw.json').read_text())
limits={r['component']:r['color_limits'] for r in fixed['rows']}
metric_values={'interpolation':[], 'rformer':[]}
invalid_counts=[]
def interpolate(x,v,grid):
    result=LinearNDInterpolator(x,v)(grid)
    missing=~np.isfinite(result).all(axis=1)
    if missing.any():result[missing]=NearestNDInterpolator(x,v)(grid[missing])
    assert np.isfinite(result).all()
    return result
meta={'source':str(raw),'averaged_source':str(averaged),'frame_interval_ms':250,'frame_count':20,'raw_indices':list(range(20)),'averaged_indices':list(range(80,100)),'alignment_source':str(RF/'results/case3_blood/dpd-averaged/analysis_publication.ipynb'),'midplane_z_tolerance':1.,'color_limits':limits,'display_extent':[-6.,306.,-54.,54.],'frames':[],'slurm_job':os.environ['SLURM_JOB_ID']}
for idx in range(20):
    avg_idx=80+idx
    with h5py.File(raw) as f:
        obs_x=f['x'][idx];obs_v=f['v'][idx];qx=f['qx'][idx];qv=f['qv'][idx];pred=f['pred_q'][idx]
    with h5py.File(averaged) as f:
        avg_x=f['x'][avg_idx];avg_v=f['q'][avg_idx]
    print(f'Interpolating frame {idx+1}/20',flush=True)
    obs_grid=interpolate(obs_x,obs_v,avg_x)
    rec_grid=interpolate(qx,pred,avg_x)
    common=np.isfinite(avg_v).all(axis=1)&(np.abs(avg_v)<=10).all(axis=1)
    invalid_counts.append(int((~common).sum()))
    target=avg_v[common].astype(np.float64)
    denominator=np.linalg.norm(target)
    assert denominator>0
    for name,value in [('interpolation',obs_grid),('rformer',rec_grid)]:
        metric_values[name].append(float(np.linalg.norm(value[common].astype(np.float64)-target)/denominator))
    coords=[obs_x,avg_x,avg_x,avg_x]
    fields=[obs_v,obs_grid,rec_grid,avg_v]
    masks=[np.abs(x[:,2])<1 for x in coords]
    for j in [1,2,3]:masks[j]=masks[j]&common
    frame={'raw_index':idx,'averaged_index':avg_idx,'panels':[]}
    for channel,component in enumerate(['u','v']):
        vmin,vmax=limits[component]
        for j,(x,v,m) in enumerate(zip(coords,fields,masks)):
            m=m&np.isfinite(v[:,channel]);x=x[m,:2];v=v[m,channel]
            assert np.isfinite(x).all()
            fig=plt.figure(figsize=(3.12,1.08),dpi=200);ax=fig.add_axes([0,0,1,1])
            ax.scatter(x[:,0],x[:,1],c=v,cmap='coolwarm',norm=TwoSlopeNorm(vcenter=0,vmin=vmin,vmax=vmax),s=[2.5,.45,.45,.45][j],linewidths=0)
            ax.set(xlim=(-6,306),ylim=(-54,54));ax.set_aspect('equal');ax.set_axis_off()
            p=out/f'{idx:03d}-{component}-{j}.png';fig.savefig(p,dpi=200,facecolor='white');plt.close(fig)
            frame['panels'].append({'path':str(p),'point_count':len(v),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    meta['frames'].append(frame);print(f'Rendered {idx+1}/20 matched frames',flush=True)
meta['columns']=['Sparse observations','Linear interpolation','RFormer reconstruction','Averaged-grid reference']
meta['interpolation_method']='3D linear; nearest-neighbor fill outside convex hull; recomputed from val.h5 at each matched averaged grid'
meta['metrics']={'definition':'norm(pred-reference)/norm(reference), full 3D velocity vector on a shared reference-valid mask: finite components within [-10,10], per snapshot; no clipping', 'snapshot_count':20, 'invalid_reference_counts':invalid_counts, 'reference_validity_range':[-10,10], 'validity_range_source':str(RF/'results/case3_blood/dpd-averaged/analysis_publication.ipynb'), 'methods':{name:{'per_snapshot':values,'mean':float(np.mean(values)),'std':float(np.std(values))} for name,values in metric_values.items()}}
print(json.dumps(meta['metrics'],indent=2),flush=True)
(out/'index.json').write_text(json.dumps(meta,indent=2)+'\n')
publish('blood',meta,lambda path:out/Path(path).name)
with open(f'/tmp/{os.environ["USER"]}.agent-lock','a') as lock:
    fcntl.flock(lock,fcntl.LOCK_EX)
    for p in out.glob('005-*.png'):
        shutil.copyfile(p,ROOT/'public/figures/ch06'/p.name.replace('005-','blood-'))
    fixed['columns']=meta['columns']
    fixed['interpolation_method']=meta['interpolation_method']
    fixed['slurm_job']=meta['slurm_job']
    for channel,row in enumerate(fixed['rows']):
        row['panels']=[dict(panel,path=f'/figures/ch06/blood-{row["component"]}-{j}.png') for j,panel in enumerate(meta['frames'][5]['panels'][channel*4:channel*4+4])]
    (ROOT/'public/data/ch06/blood-redraw.json').write_text(json.dumps(fixed,indent=2)+'\n')

print('Published 20 synchronized eight-panel frames.',flush=True)
