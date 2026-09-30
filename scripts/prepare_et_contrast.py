"""Set an explicit reference-range color scale; retain actual values/metrics."""
import os,json,hashlib,shutil
from pathlib import Path
from datetime import datetime,timezone
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1];assert os.environ.get('SLURM_JOB_ID')
mp=root/'public/data/manifest.json';m=json.loads(mp.read_text());entry=next(a for a in m['assets'] if a['chapter']=='ch05')
p=json.loads((mp.parent/entry['path']).read_text())['data']['states'][0]['payload']
def arr(k):return np.asarray(p[k]['values']).reshape(p[k]['shape'])
ref=arr('reference');frames=arr('frames');lo,hi=float(ref.min()),float(ref.max())
fig,axes=plt.subplots(1,4,figsize=(13,3.1),layout='constrained')
for ax,v,title in zip(axes,[ref,frames[0],frames[5],frames[-1]],['Reference','Update 1','Update 6','Update 12']):
    outside=100*np.mean((v<lo)|(v>hi))
    im=ax.imshow(v,origin='lower',cmap='RdBu_r',vmin=lo,vmax=hi,interpolation='nearest')
    ax.set_title(title+f'\n{outside:.1f}% outside color range',fontsize=10);ax.set_xlabel('column index')
axes[0].set_ylabel('row index');fig.colorbar(im,ax=axes,shrink=.8,label='normalized v · fixed reference range',extend='both')
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')+'-contrast-'+os.environ['SLURM_JOB_ID'];out=mp.parent/'releases'/stamp/'ch05';out.mkdir(parents=True)
png=out/'energy_history.png';fig.savefig(png,dpi=180);plt.close(fig)
shutil.copyfile(png,root/'public/fallback_figures/ch05/energy_history.png')
entry['fallback_path']='/'+str(png.relative_to(root/'public'));entry['fallback_sha256']=hashlib.sha256(png.read_bytes()).hexdigest()
mp.write_text(json.dumps(m,indent=2)+'\n')
