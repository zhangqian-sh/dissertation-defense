"""Export every other saved day of weather predictions with fixed [-30, 40] °C display limits. CPU-only Slurm job; no model inference."""
from animation_bundle import publish
import os,json,hashlib,shutil
from pathlib import Path
from datetime import date,timedelta
import numpy as np
import h5py
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from scipy.ndimage import gaussian_filter
import geopandas as gpd
from shapely import contains_xy

assert os.environ.get('SLURM_JOB_ID'), 'Use Slurm'
ROOT=Path(__file__).resolve().parents[1]
RF=Path('/oscar/data/gk/qzhang64/Projects/OperatorLearning/RFormer/reproducibility')
from matplotlib.font_manager import fontManager
fontManager.addfont(str(ROOT/'public/fonts/NotoSerif-Regular.ttf'))
plt.rcParams.update({'font.family':'Noto Serif','mathtext.fontset':'cm','font.size':12,'axes.unicode_minus':False,'axes.spines.top':True,'axes.spines.right':True})
def digest(p):
    with open(p,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def begin(name):
    out=ROOT/'data/staging'/f'weather-export-{os.environ["SLURM_JOB_ID"]}'/name;out.mkdir(parents=True,exist_ok=True);return out,[]
def frame(out,entries,fig):
    p=out/f'{len(entries):03d}.png';fig.savefig(p,dpi=130,facecolor='white');plt.close(fig)
    entries.append({'path':str(p),'sha256':digest(p)})
def finish(out,entries,times,labels,caption,sources=(),**extra):
    assert len(entries)==len(times)==len(labels) and np.all(np.diff(times)>0)
    meta=dict(frames=entries,times=list(map(float,times)),labels=labels,caption=caption,sources=[{'path':str(p),'sha256':digest(p)} for p in sources],slurm_job=os.environ['SLURM_JOB_ID'],**extra)
    (out/'index.json').write_text(json.dumps(meta,indent=2)+'\n');print(out.name,len(entries),flush=True)

# NOAA station predictions: 183 snapshots, every other day of 2024; spatial
# display interpolation only, masked to US land and station convex hull.
out,entries=begin('weather');out=ROOT/'data/staging'/f'weather-daily-{os.environ["SLURM_JOB_ID"]}';out.mkdir(parents=True,exist_ok=True);src=RF/'results/case2/run-001/test.h5'
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
days=np.arange(0,366,2);vmin,vmax=-30.,40.
raw_range=[float(min(values.min(),reference.min())),float(max(values.max(),reference.max()))]
def render_day(day):
    fig,axes=plt.subplots(2,1,figsize=(8,9),constrained_layout=True)
    for ax,field,title in zip(axes,[reference,values],['Reference','Reconstructed']):
        z=griddata(x,field[day],(gx,gy),method='linear');valid=np.isfinite(z)
        z=gaussian_filter(np.nan_to_num(z),1.2)/np.maximum(gaussian_filter(valid.astype(float),1.2),1e-12)
        z[~(land&valid)]=np.nan
        im=ax.imshow(z,extent=[-125,-66,24,50],origin='lower',cmap='coolwarm',vmin=vmin,vmax=vmax,aspect='auto')
        gpd.GeoSeries([us]).boundary.plot(ax=ax,color='#424c4b',linewidth=.5)
        ax.set(xlim=(-125,-66),ylim=(24,50),xlabel='Longitude',ylabel='Latitude',title=title)
        # GeoPandas sets its own geographic aspect; restore the requested panel shape.
        ax.set_aspect('auto')
        ax.set_box_aspect(1/1.7)
    fig.colorbar(im,ax=axes,label='Daily mean temperature (°C)',fraction=.035,pad=.02)
    p=out/f'{day:03d}.png'
    fig.savefig(p,dpi=130,facecolor='white');plt.close(fig)
    return {'path':str(p),'sha256':digest(p)}
from concurrent.futures import ProcessPoolExecutor
with ProcessPoolExecutor(max_workers=2) as pool:
    for entry in pool.map(render_day,days):
        entries.append(entry)
        if len(entries)%25==0: print(f"Rendered {len(entries)}/{len(days)} snapshots",flush=True)

finish(out,entries,days,[str(date(2024,1,1)+timedelta(days=int(i))) for i in days],'Every other day of 2024 (183 snapshots); fixed temperature scale [-30, 40] °C.',[src,truth,geo],columns=['Reference','Reconstructed'],reference_type='Paired validation station measurements, not gridded ground truth',spatial_smoothing='linear station interpolation then normalized Gaussian sigma=1.2 pixels; mask outside US land/station hull',source_preprocessing='Missing station days filled by source temporal preprocessing',color_limits=[vmin,vmax],raw_range=raw_range,color_qualification='Fixed display saturation only; values unchanged; no additional source quality control')


import fcntl
with open(f'/tmp/{os.environ["USER"]}.agent-lock','a') as lock:
    fcntl.flock(lock,fcntl.LOCK_EX)
    fallback=ROOT/'public/fallback_figures/sequences/weather.png'
    shutil.copyfile(out/'000.png',fallback)

publish('weather',json.loads((out/'index.json').read_text()),lambda path:out/Path(path).name)
print('Published lossless alternate-day weather bundle and first-day fallback.',flush=True)
