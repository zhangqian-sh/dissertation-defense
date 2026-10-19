"""Refresh only Poisson display scales and its PDF fallback; do not rerun the SNN."""
from pathlib import Path
import os, json, hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.font_manager import fontManager

ROOT=Path(__file__).resolve().parents[1]

def render_fallback(root,payload,frames):
    fontManager.addfont(str(root/'public/fonts/NotoSerif-Regular.ttf'))
    plt.rcParams['font.family']='Noto Serif'
    plt.rcParams['axes.unicode_minus']=False
    reference=np.asarray(payload['reference']['values']).reshape(payload['reference']['shape'])
    # Match the jet colormap on the preceding Poisson slide.
    solution=difference=plt.get_cmap('jet')
    fig,axes=plt.subplots(1,3,figsize=(12,3.9),layout='constrained')
    for axis,values,title,cmap,lo,hi in zip(axes,[reference,frames[-1],frames[-1]-reference],
            ['ANN reference','SNN · spike step 64','Difference · SNN - ANN'],
            [solution,solution,difference],[0,0,-.03],[.32,.32,.03]):
        im=axis.imshow(values,origin='lower',extent=[-1,1,-1,1],cmap=cmap,vmin=lo,vmax=hi,interpolation='nearest')
        axis.set(title=title,xlabel='x',ylabel='y')
        bar=fig.colorbar(im,ax=axis,shrink=.76,extend='both' if lo<0 else 'neither')
        bar.set_ticks([lo,(lo+hi)/2,hi])
    error=payload['relative_error']['values'][-1]
    fig.suptitle(f'Fixed calibration at T = 64 · relative L₂ vs ANN: {error:.4f} · error colors saturate beyond ±0.03',fontsize=10)
    path=root/'public/fallback_figures/ch03/poisson_prefix.png'
    fig.savefig(path,dpi=170);plt.close(fig)
    return path

if __name__=='__main__':
    assert os.environ.get('SLURM_JOB_ID'),'Run figure generation in Slurm'
    path=ROOT/'public/data/sequences/poisson-prefix.json'
    envelope=json.loads(path.read_text());payload=envelope['data']['states'][0]['payload']
    payload.update(field_min=0.0,field_max=0.32,difference_limit=0.03)
    frames=np.fromfile(ROOT/'public'/payload['frames']['binary_path'].lstrip('/'),dtype='<f4').reshape(payload['frames']['shape'])
    fallback=render_fallback(ROOT,payload,frames)
    path.write_text(json.dumps(envelope,separators=(',',':'))+'\n')
    manifest_path=ROOT/'public/data/manifest.json';manifest=json.loads(manifest_path.read_text())
    entry=next(a for a in manifest['assets'] if a['asset_id']=='ch03/poisson_prefix')
    entry['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
    entry['fallback_sha256']=hashlib.sha256(fallback.read_bytes()).hexdigest()
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    print('Updated fixed Poisson scales and PDF fallback; numerical arrays unchanged.')
