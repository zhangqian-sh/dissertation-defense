"""Animate the saved hybrid RFormer predictions using the original notebook plot (Slurm CPU only)."""
from animation_bundle import publish, digest
import os,json
from pathlib import Path
import h5py,numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from matplotlib.font_manager import fontManager
assert os.environ.get('SLURM_JOB_ID'),'Run through Slurm'
ROOT=Path(__file__).resolve().parents[1]
RUN=Path('/oscar/data/gk/qzhang64/Projects/SpikingNN/SpikeCalibTransformer/runs/rformer/rformer_full')
RF=Path('/oscar/data/gk/qzhang64/Projects/OperatorLearning/RFormer/reproducibility')
src=RUN/'predictions/snn_test_predictions.h5';ann=RF/'results/case1/run-001/test.h5'
out=ROOT/'data/staging'/f'hybrid-rformer-{os.environ["SLURM_JOB_ID"]}';out.mkdir(parents=True,exist_ok=True)
with h5py.File(src) as f:data={key:f[key][:] for key in ['x','v','qx','qv','pred_q']}
assert data['pred_q'].shape==data['qv'].shape==(20,28668,3)
assert data['v'].shape==(20,512,3)
assert all(np.isfinite(value).all() for value in data.values())
with h5py.File(ann) as f:
 for key in ['x','v','qx','qv']:np.testing.assert_array_equal(data[key],f[key][:])
times=[]
for i in range(20):
 with (RF/f'data/case1_vortex_street/raw/uvtp_data_{80+i}.csv').open() as f:
  next(f);times.append(float(next(f).split(',')[0]))
order=np.argsort(times);times=np.asarray(times)[order]
assert np.all(np.diff(times)>0)
# The original notebook uses reference-wide 1st/99th percentiles. Fixed contour
# levels, not an automatic per-frame choice, make colors comparable across time.
vmin=np.percentile(data['qv'],1,axis=(0,1));vmax=np.percentile(data['qv'],99,axis=(0,1))
fontManager.addfont(str(ROOT/'public/fonts/NotoSerif-Regular.ttf'))
plt.rcParams.update({'font.family':'Noto Serif','mathtext.fontset':'cm','axes.unicode_minus':False})
entries=[]
for frame,row in enumerate(order):
 fig,axes=plt.subplots(3,3,figsize=(14,7),constrained_layout=False)
 row_mappables=[]
 for c,name in enumerate(['u','v','p']):
  xy=data['qx'][row];obs=data['x'][row];levels=np.linspace(vmin[c],vmax[c],20)
  for col,title in enumerate([f'True {name}','Observed','SNN Reconstructed']):
   ax=axes[c,col]
   if col==1:
    im=ax.scatter(obs[:,0],obs[:,1],c=data['v'][row,:,c],s=1,cmap='coolwarm',vmin=vmin[c],vmax=vmax[c])
   else:
    values=data['qv' if col==0 else 'pred_q'][row,:,c]
    im=ax.tricontourf(xy[:,0],xy[:,1],values,levels=levels,cmap='coolwarm',vmin=vmin[c],vmax=vmax[c],extend='both')
    if col==0:row_mappables.append(im)
   ax.set_title(title,fontsize=21,pad=6)
   ax.add_patch(plt.Circle((0,0),.5,color='white',fill=True))
   ax.set_aspect('equal');ax.set_xticks([]);ax.set_yticks([])
   ax.set_xlim(xy[:,0].min(),xy[:,0].max());ax.set_ylim(xy[:,1].min(),xy[:,1].max())
 fig.subplots_adjust(left=.03,right=.88,bottom=.04,top=.94,wspace=.08,hspace=.22)
 for c,im in enumerate(row_mappables):
  y0=min(ax.get_position().y0 for ax in axes[c]);y1=max(ax.get_position().y1 for ax in axes[c])
  cax=fig.add_axes([.90,y0,.018,y1-y0]);bar=fig.colorbar(im,cax=cax,extendrect=True)
  bar.set_ticks(np.linspace(vmin[c],vmax[c],5));bar.ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'));bar.ax.tick_params(labelsize=11)
 path=out/f'hybrid-{frame:03d}.png';fig.savefig(path,dpi=150,facecolor='white')
 panel_bounds=[[[float(x),float(1-y-h),float(w),float(h)] for x,y,w,h in [ax.get_position().bounds for ax in row_axes]] for row_axes in axes]
 plt.close(fig)
 entries.append({'path':str(path),'sha256':digest(path)})
 print('Rendered',frame+1,'/ 20',flush=True)
meta={'case':'hybrid','source':str(src),'source_sha256':digest(src),'reference_source':str(ann),'reference_sha256':digest(ann),'frames':entries,'times':times.tolist(),'source_rows':order.tolist(),'rows':['u','v','p'],'columns':['Reference','Observations','Hybrid SNN'],'spike_steps':32,'panel_bounds':panel_bounds,'field_limits':np.column_stack([vmin,vmax]).tolist(),'color_policy':'Fixed reference-wide 1st/99th percentiles per component; fixed 20 contour levels across all snapshots; saturated extremes.','plot_source':'SpikeCalibTransformer/runs/rformer/converted_snn_analysis.ipynb, snapshot reconstruction cell','slurm_job':os.environ['SLURM_JOB_ID']}
(out/'index.json').write_text(json.dumps(meta,indent=2)+'\n')
published=publish('hybrid',meta,lambda path:out/Path(path).name)
print('Published',len(entries),'snapshots;',published['bundle']['byte_length'],'bytes',flush=True)
