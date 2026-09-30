"""Recorded weather and optimized trajectories, with published blood snapshots."""
import os,json,hashlib,subprocess
from pathlib import Path
from datetime import date,timedelta
import numpy as np
import h5py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter
from scipy.spatial.distance import pdist
import geopandas as gpd
from shapely import contains_xy

assert os.environ.get('SLURM_JOB_ID'), 'Use Slurm'
ONLY=os.environ.get('SEQUENCE_CASE')
ROOT=Path(__file__).resolve().parents[1]
RF=Path('/oscar/data/gk/qzhang64/Projects/OperatorLearning/RFormer/reproducibility')
OC=Path('/oscar/data/gk/qzhang64/Projects/OptimalControl/OCFormer')
plt.rcParams.update({'font.size':10,'axes.spines.top':True,'axes.spines.right':True})
def digest(p):
    with open(p,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def begin(name):
    out=ROOT/'public/data/sequences'/name;out.mkdir(parents=True,exist_ok=True);return out,[]
def frame(out,entries,fig):
    p=out/f'{len(entries):03d}.png';fig.savefig(p,dpi=130,facecolor='white');plt.close(fig)
    entries.append({'path':'/'+str(p.relative_to(ROOT/'public')),'sha256':digest(p)})
def finish(out,entries,times,labels,caption,sources=(),**extra):
    assert len(entries)==len(times)==len(labels) and np.all(np.diff(times)>0)
    meta=dict(frames=entries,times=list(map(float,times)),labels=labels,caption=caption,sources=[{'path':str(p),'sha256':digest(p)} for p in sources],slurm_job=os.environ['SLURM_JOB_ID'],**extra)
    (out/'index.json').write_text(json.dumps(meta,indent=2)+'\n');print(out.name,len(entries),flush=True)

# Use exactly the optimized trajectory loaded by the original paper notebook.
out,entries=begin('latent');latent_src=OC/'results/room_2d/OCFormer_-1_16/best_pred_lbfgs.h5'
with h5py.File(latent_src) as f:paths=f['q'][:].reshape(200,8,2)
times=np.linspace(0,10,len(paths));start=paths[0];end=paths[-1]
straight=np.linspace(start,end,len(paths))
assert np.isfinite(paths).all() and np.max(np.abs(start+end))<1e-3
rng=np.random.default_rng(5);colors=['#%06X'%rng.integers(0,0xFFFFFF) for _ in range(8)]
for k,t in (enumerate(times) if ONLY in [None,'latent'] else []):
    fig,axes=plt.subplots(1,2,figsize=(10,4.2));fig.subplots_adjust(wspace=.48,left=.03,right=.97,bottom=.04,top=.90)
    for j,ax in enumerate(axes):
        ax.set(title=['Latent Space','Physical Space'][j],xlim=(-.55,.55),ylim=(-.55,.55),aspect='equal',xticks=[],yticks=[])
        for a in range(8):
            line=straight[:,a] if j==0 else paths[:,a]
            ax.plot(line[:,0],line[:,1],color=colors[a],alpha=.22,lw=1.2)
            pos=straight[k,a] if j==0 else paths[k,a]
            ax.scatter(*start[a],s=45,facecolors='none',edgecolors=[colors[a]])
            ax.scatter(*pos,s=35,c=[colors[a]],zorder=4)
        if j==0 and k in [99,100]:ax.annotate('Central crossing',(0,0),xytext=(.08,.14),fontsize=9,arrowprops={'arrowstyle':'->'})
    fig.text(.5,.53,r'$\phi^{-1}\;\longrightarrow$',ha='center',fontsize=14)
    fig.text(.5,.41,r'$\longleftarrow\;\phi$',ha='center',fontsize=14)
    frame(out,entries,fig)
if entries:finish(out,entries,times,[f'{t:.2f} s' for t in times],'Left: straight endpoint reference. Right: saved L-BFGS optimized trajectories, not a hand-designed detour.',[latent_src,OC/'results/room_2d/analysis.ipynb'],illustrative=False,physical_source='saved q without interpolation',positions_shape=list(paths.shape),left_reference='linear interpolation of recorded endpoints',central_reference_max_radius=float(np.linalg.norm(straight[99:101],axis=-1).max()))

# Saved 128-drone per-instance trajectory: retain every evaluation frame.
out,entries=begin('swarm128');src=OC/'results/room_2d/OCFormer_0_256_M=128/best_pred_lbfgs.h5'
boundary=OC/'data/room_2d/n=128/boundary.h5'
with h5py.File(src) as f:q=f['q'][:].reshape(200,128,2)
with h5py.File(boundary) as f:b=f['boundary'][:].reshape(2,128,2)
assert np.isfinite(q).all() and np.max(np.abs(q[[0,-1]]-b))<.02
times=np.linspace(0,10,200);margins=np.array([pdist(x).min()-.02 for x in q])
rng=np.random.default_rng(5);colors=['#%06X'%rng.integers(0,0xFFFFFF) for _ in range(128)]
for k,t in (enumerate(times) if ONLY in [None,'swarm128'] else []):
    fig,ax=plt.subplots(figsize=(7,5),constrained_layout=True)
    for a in range(128):
        ax.plot(q[:k+1,a,0],q[:k+1,a,1],color='gray',alpha=.1,lw=1.5)
        ax.add_patch(plt.Circle(q[k,a],.01,fill=False,color=colors[a],lw=1))
    ax.set_xticks(np.linspace(-.5,.5,5));ax.set_yticks(np.linspace(-.5,.5,5))
    ax.set(xlim=(-.52,.52),ylim=(-.52,.52),aspect='equal',xlabel='x',ylabel='y',title=f'128 drones · t = {t:.2f} s')
    ax.text(.02,.02,f'Sampled pairwise clearance: {margins[k]:.4f}',transform=ax.transAxes,fontsize=9)
    frame(out,entries,fig)
if entries:finish(out,entries,times,[f'{t:.2f} s' for t in times],'Saved per-instance OCFormer · 128 drones · sampled constraints only; not continuous-time safety.',[src,boundary,OC/'results/room_2d/notebooks/pub-path-time.ipynb'],agent_count=128,minimum_pairwise_clearance=float(margins.min()),positions_shape=list(q.shape),paper_colors=colors,paper_style='default_rng(5) hex palette; hollow radius .01 circles; cumulative gray trajectories alpha .1')

# NOAA station predictions: weekly recorded days (plus year end), spatial
# display interpolation only, masked to US land and station convex hull.
out,entries=begin('weather');src=RF/'results/case2/run-001/test.h5'
with h5py.File(src) as f:
    x=np.concatenate([f['x'][0],f['qx'][0]])[:,::-1]
    values=np.concatenate([f['v'][:],f['pred_q'][:]],axis=1)[:,:,0]
    truth=RF/'data/case2_weather/processed/valid.h5'
    with h5py.File(truth) as g:
        for key in ['x','qx','v']:np.testing.assert_array_equal(f[key][:],g[key][:])
        reference=np.concatenate([g['v'][:],g['qv'][:]],axis=1)[:,:,0]
assert values.shape==(366,2020) and np.isfinite(values).all()
geo=RF/'data/case2_weather/raw/ne_110m_admin_0_countries.zip'
world=gpd.read_file('zip://'+str(geo));us=world[world['ADMIN']=='United States of America'].geometry.iloc[0]
gx,gy=np.meshgrid(np.linspace(-125,-66,650),np.linspace(24,50,300));land=contains_xy(us,gx,gy)
days=np.unique(np.r_[np.arange(0,366,7),365]);vmin,vmax=-40.,45.
raw_range=[float(min(values.min(),reference.min())),float(max(values.max(),reference.max()))]
for day in days:
    fig,axes=plt.subplots(2,1,figsize=(8,7),constrained_layout=True)
    for ax,field,title in zip(axes,[reference,values],['Reference','Reconstructed']):
        z=griddata(x,field[day],(gx,gy),method='linear');valid=np.isfinite(z)
        z=gaussian_filter(np.nan_to_num(z),1.2)/np.maximum(gaussian_filter(valid.astype(float),1.2),1e-12)
        z[~(land&valid)]=np.nan
        im=ax.imshow(z,extent=[-125,-66,24,50],origin='lower',cmap='coolwarm',vmin=vmin,vmax=vmax,aspect='auto')
        gpd.GeoSeries([us]).boundary.plot(ax=ax,color='#424c4b',linewidth=.5)
        outside=int(np.count_nonzero((field[day]<vmin)|(field[day]>vmax)))
        ax.set(xlim=(-125,-66),ylim=(24,50),xlabel='Longitude',ylabel='Latitude',title=f'{title} · {outside} station values outside color range')
    fig.colorbar(im,ax=axes,label='Daily mean temperature (°C)',fraction=.035,pad=.02)
    frame(out,entries,fig)
finish(out,entries,days,[str(date(2024,1,1)+timedelta(days=int(i))) for i in days],'2024 recorded days · reference and reconstructed station fields · shared spatial interpolation and °C scale.',[src,truth,geo],columns=['Reference','Reconstructed'],reference_type='Paired validation station measurements, not gridded ground truth',spatial_smoothing='linear station interpolation then normalized Gaussian sigma=1.2 pixels; mask outside US land/station hull',source_preprocessing='Missing station days filled by source temporal preprocessing',color_limits=[vmin,vmax],raw_range=raw_range,color_qualification='Fixed display saturation only; values unchanged; per-frame station outlier counts labeled; no additional source quality control')

# User requested the original static u/v snapshot figures, replacing playback.
snapshot_out=ROOT/'public/figures/ch06';sources=[]
for component in ['u','v']:
    pdf=RF.parent/f'publication/manuscript/figures/experiments/blood_flow/blood_snapshot_{component}.pdf'
    output=snapshot_out/f'blood-snapshot-{component}'
    subprocess.run(['pdftoppm','-png','-singlefile','-scale-to','1800',str(pdf),str(output)],check=True)
    sources.append({'source':str(pdf),'sha256':digest(pdf),'output':str(output.with_suffix('.png').relative_to(ROOT)),'output_sha256':digest(output.with_suffix('.png'))})
(ROOT/'docs/blood_snapshot_sources.json').write_text(json.dumps(sources,indent=2)+'\n')
