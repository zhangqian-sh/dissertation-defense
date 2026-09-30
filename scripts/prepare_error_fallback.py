"""Publish an error-focused static view of the existing, unchanged SNN data."""
from pathlib import Path
import json, hashlib, shutil, os
from datetime import datetime, timezone
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.tri import Triangulation, LinearTriInterpolator
root=Path(__file__).resolve().parents[1]
assert os.environ.get('SLURM_JOB_ID')
mp=root/'public/data/manifest.json';manifest=json.loads(mp.read_text())
entry=next(a for a in manifest['assets'] if a['asset_id']=='ch03/conversion_over_t')
p=json.loads((mp.parent/entry['path']).read_text())['data']['states'][0]['payload']
def array(k):
    t=p[k];return np.asarray(t['values']).reshape(t['shape'])
xy=array('coordinates');tri=Triangulation(xy[:,0],xy[:,1],array('mesh_cells').astype(int))
fields=array('field_prefix_output')-array('ann_output')
grid=np.meshgrid(np.linspace(xy[:,0].min(),xy[:,0].max(),256),np.linspace(xy[:,1].min(),xy[:,1].max(),256))
limit=np.abs(fields).max();fig,axes=plt.subplots(1,4,figsize=(14,3.4),layout='constrained')
for ax,step in zip(axes[:3],[0,7,63]):
    v=LinearTriInterpolator(tri,fields[step])(*grid)
    im=ax.imshow(v,origin='lower',extent=[xy[:,0].min(),xy[:,0].max(),xy[:,1].min(),xy[:,1].max()],cmap='RdBu_r',vmin=-limit,vmax=limit)
    ax.set_title(f'SNN − ANN · prefix {step+1}');ax.set_xlabel('x')
axes[0].set_ylabel('y');fig.colorbar(im,ax=list(axes[:3]),shrink=.7,label='signed conversion error')
axes[3].plot(np.arange(1,65),array('reference_error'),label='vs reference',color='#287e83')
axes[3].plot(np.arange(1,65),array('conversion_error'),label='vs ANN',color='#8b242d')
axes[3].set(xlabel='internal prefix length',ylabel='relative L₂');axes[3].legend(fontsize=8);axes[3].grid(alpha=.2)
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')+'-error-'+os.environ['SLURM_JOB_ID']
out=mp.parent/'releases'/stamp/'ch03';out.mkdir(parents=True)
png=out/'conversion_over_t.png';fig.savefig(png,dpi=160);plt.close(fig)
shutil.copyfile(png,root/'public/fallback_figures/ch03/conversion_over_t.png')
entry['fallback_path']='/'+str(png.relative_to(root/'public'))
entry['fallback_sha256']=hashlib.sha256(png.read_bytes()).hexdigest()
manifest['generated_at']=datetime.now(timezone.utc).isoformat();mp.write_text(json.dumps(manifest,indent=2)+'\n')
print('Published smooth SNN error fallback:',png)
