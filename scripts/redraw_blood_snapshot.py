"""Redraw the published blood snapshot into eight data panels (Slurm CPU only).

Source: prev/results/case3_blood/dpd-averaged/analysis_publication.ipynb.
Same snapshot 5, averaged snapshot 85, |z|<1 plane, and shared 99th-percentile
symmetric color limits per component. Native slide text supplies axes and labels.
"""
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
idx=5;avg_idx=85
out=ROOT/'data/staging'/f'blood-redraw-{os.environ["SLURM_JOB_ID"]}';out.mkdir(parents=True,exist_ok=True)
with h5py.File(raw) as f:
    obs_x=f['x'][idx];obs_v=f['v'][idx];qx=f['qx'][idx];qv=f['qv'][idx];pred=f['pred_q'][idx]
with h5py.File(averaged) as f:
    avg_x=f['x'][avg_idx];avg_v=f['q'][avg_idx]
def interpolate(x,v,grid):
    result=LinearNDInterpolator(x,v)(grid)
    missing=~np.isfinite(result).all(axis=1)
    if missing.any():result[missing]=NearestNDInterpolator(x,v)(grid[missing])
    return result
coords=[obs_x,avg_x,avg_x,avg_x]
fields=[obs_v,interpolate(obs_x,obs_v,avg_x),interpolate(qx,pred,avg_x),avg_v]
masks=[np.abs(x[:,2])<1 for x in coords]
common=np.isfinite(avg_v).all(axis=1)&(np.abs(avg_v)<=10).all(axis=1)
for j in [1,2,3]:masks[j]=masks[j]&common
extent=[-6.,306.,-54.,54.]
meta={'source':str(raw),'averaged_source':str(averaged),'snapshot':idx,'averaged_snapshot':avg_idx,'midplane_z_tolerance':1.,'display_extent':extent,'columns':['Sparse observations','Linear interpolation','RFormer reconstruction','Averaged-grid reference'],'rows':[],'slurm_job':os.environ['SLURM_JOB_ID']}
for channel,component in enumerate(['u','v']):
    panels=[]
    for x,v,m in zip(coords,fields,masks):
        m=m&np.isfinite(v[:,channel]);panels.append((x[m,:2],v[m,channel]))
    vmax=json.loads((ROOT/'public/data/ch06/blood-redraw.json').read_text())['rows'][channel]['color_limits'][1]
    assert np.isfinite(vmax) and vmax>0
    row={'component':component,'color_limits':[-vmax,vmax],'panels':[]}
    for j,(x,v) in enumerate(panels):
        fig=plt.figure(figsize=(3.12,1.08),dpi=300);ax=fig.add_axes([0,0,1,1])
        ax.scatter(x[:,0],x[:,1],c=v,cmap='coolwarm',norm=TwoSlopeNorm(vcenter=0,vmin=-vmax,vmax=vmax),s=[2.5,.45,.45,.45][j],linewidths=0)
        ax.set(xlim=extent[:2],ylim=extent[2:]);ax.set_aspect('equal');ax.set_axis_off()
        p=out/f'blood-{component}-{j}.png';fig.savefig(p,dpi=300,facecolor='white');plt.close(fig)
        row['panels'].append({'path':f'/figures/ch06/{p.name}','point_count':len(v),'points_sha256':hashlib.sha256(x.tobytes()).hexdigest(),'values_sha256':hashlib.sha256(v.tobytes()).hexdigest(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    meta['rows'].append(row)
    print(component,'color limits',[-vmax,vmax],'point counts',[p['point_count'] for p in row['panels']],flush=True)
(out/'blood-redraw.json').write_text(json.dumps(meta,indent=2)+'\n')
with open(f'/tmp/{os.environ["USER"]}.agent-lock','a') as lock:
    fcntl.flock(lock,fcntl.LOCK_EX)
    for p in out.glob('*.png'):shutil.copyfile(p,ROOT/'public/figures/ch06'/p.name)
    shutil.copyfile(out/'blood-redraw.json',ROOT/'public/data/ch06/blood-redraw.json')
print('Published eight redrawn blood panels.',flush=True)
