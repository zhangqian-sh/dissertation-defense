"""Export saved RFormer snapshots in verified physical-time order (Slurm only)."""
from animation_bundle import publish
import os, json, hashlib, shutil, fcntl
from pathlib import Path
import h5py
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.interpolate import griddata

assert os.environ.get('SLURM_JOB_ID'), 'Run through Slurm'
ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path('/oscar/data/gk/qzhang64/Projects/OperatorLearning/RFormer/reproducibility')
OUT = Path(os.environ.get('RFORMER_OUTPUT', ROOT / 'data/staging' / f'rformer-time-{os.environ["SLURM_JOB_ID"]}'))
OUT.mkdir(parents=True, exist_ok=True)
sha = lambda p: hashlib.file_digest(open(p, 'rb'), 'sha256').hexdigest()
for case, run, channel in [('vortex', 'case1', 1), ('jet', 'case4', 1)]:
    src = SOURCE / f'results/{run}/run-001/test.h5'
    with h5py.File(src) as f:
        n_obs = f['x'].shape[1]
        coords = np.concatenate([f['x'][:], f['qx'][:]], axis=1)
        ref = np.concatenate([f['v'][:], f['qv'][:]], axis=1)
        # Observation-token predictions are discarded by the source protocol.
        # Preserve measured observations and reconstruct only query positions.
        pred = np.concatenate([f['v'][:], f['pred_q'][:]], axis=1)
    truth_source = src
    if case == 'jet':
        # The test queries are deliberately blinded; use the paired validation
        # truth only after checking coordinates and observed values exactly.
        truth_source = SOURCE / 'data/case3_turbulent_jet/processed/valid.h5'
        with h5py.File(truth_source) as f:
            np.testing.assert_array_equal(coords, np.concatenate([f['x'][:],f['qx'][:]],axis=1))
            np.testing.assert_array_equal(ref[:,:f['v'].shape[1]], f['v'][:])
            ref = np.concatenate([f['v'][:],f['qv'][:]],axis=1)
    assert coords.shape[:2] == ref.shape[:2] == pred.shape[:2]
    if case == 'vortex':
        times = []
        for i in range(len(ref)):
            raw = SOURCE / f'data/case1_vortex_street/raw/uvtp_data_{80+i}.csv'
            times.append(float(raw.open().readlines()[1].split(',')[0]))
        qualifier = 'u, v, p rows; Reference, Observations, RFormer columns · 512 measured observations'
        extent = [-4, 12, -4, 4]
    else:
        raw = SOURCE / 'data/case3_turbulent_jet/raw/tracks.h5'
        with h5py.File(raw) as f:
            tracks = f['tracks'][:].astype(np.float32)
        times = []
        for i in range(len(ref)):
            key = np.concatenate([coords[i, 0], ref[i, 0]]).astype(np.float32)
            matches = np.all(np.isclose(tracks[:, :6], key, rtol=1e-6, atol=1e-6), axis=1)
            t = np.unique(tracks[matches, 8])
            assert len(t) == 1, (i, t)
            times.append(float(t[0]))
        qualifier = '(u,v) vectors at native points · |z| < 5 slab · measured observation vectors · fixed arrow scale'
        extent = [-15, 15, -30, 40]
    order = np.argsort(times)
    times = np.asarray(times)[order]
    assert np.all(np.diff(times) > 0)
    ref, pred, coords = ref[order], pred[order], coords[order]
    limits = np.maximum(np.max(np.abs(ref),axis=(0,1)),np.max(np.abs(pred),axis=(0,1)))
    assert np.isfinite(ref).all() and np.isfinite(pred).all()
    gx, gy = np.meshgrid(np.linspace(-4,12,384),np.linspace(-4,4,192))
    entries = []
    for i, (x,a,b) in enumerate(zip(coords,ref,pred)):
        if case == 'vortex':
            fig,axes=plt.subplots(3,3,figsize=(12,5.8),constrained_layout=True)
            for c,name in enumerate(['u','v','p']):
                for j,title in enumerate(['Reference','Observations','RFormer']):
                    ax=axes[c,j]
                    if j==1:
                        im=ax.scatter(x[:n_obs,0],x[:n_obs,1],c=a[:n_obs,c],s=4,cmap='RdBu_r',vmin=-limits[c],vmax=limits[c],linewidths=0)
                    else:
                        values=griddata(x[:,:2],(a if j==0 else b)[:,c],(gx,gy),method='linear')
                        values[gx*gx+gy*gy<.25]=np.nan
                        im=ax.imshow(values,origin='lower',extent=extent,cmap='RdBu_r',vmin=-limits[c],vmax=limits[c],interpolation='none',aspect='equal')
                    ax.set_xlim(extent[:2]);ax.set_ylim(extent[2:]);ax.set_aspect('equal')
                    ax.set_xticks([0,5,10]);ax.set_yticks([-2,0,2]);ax.tick_params(labelsize=8)
                    if c==0:ax.set_title(title,fontsize=12)
                    if j==0:ax.set_ylabel(name+' · y',fontsize=11)
                    if c==2:ax.set_xlabel('x',fontsize=9)
                cb=fig.colorbar(im,ax=axes[c,:],fraction=.015,pad=.012)
                cb.ax.tick_params(labelsize=8)
        else:
            fig,axes=plt.subplots(1,3,figsize=(9,4.6),constrained_layout=True)
            inside=(np.abs(x[:,2])<5)&(x[:,0]>=-15)&(x[:,0]<=15)&(x[:,1]>=-30)&(x[:,1]<=40)
            ids=np.flatnonzero(inside)
            # Same deterministic native-point subset for reference/reconstruction.
            ids=ids[::max(1,int(np.ceil(len(ids)/900)))]
            obs_ids=np.flatnonzero(inside & (np.arange(len(x))<n_obs))
            assert len(obs_ids)>0
            for ax,title,values,sel in zip(axes,['Reference','Observations','RFormer'],[a,a,b],[ids,obs_ids,ids]):
                q=ax.quiver(x[sel,0],x[sel,1],values[sel,0],values[sel,1],angles='xy',scale_units='xy',scale=.08,width=.003,color='#263737')
                ax.quiverkey(q,.68,1.035,.2,'0.2',labelpos='E',coordinates='axes',fontproperties={'size':8})
                ax.set_title(title,fontsize=12,pad=24)
                ax.set_xlim(extent[:2]);ax.set_ylim(extent[2:]);ax.set_aspect('equal')
                ax.set_xlabel('x');ax.set_ylabel('y');ax.tick_params(labelsize=9)
        path=OUT/f'{case}-{i:03d}.png'
        fig.savefig(path,dpi=160,facecolor='white'); plt.close(fig)
        entries.append({'path':str(path),'sha256':sha(path)})
    meta={'case':case,'source':str(src),'source_sha256':sha(src),'reference_source':str(truth_source),'reference_sha256':sha(truth_source),'times':times.tolist(),'source_rows':order.tolist(),'frames':entries,'qualifier':qualifier,'columns':['Reference','Observations','RFormer'],'rows':['u','v','p'] if case=='vortex' else ['velocity'],'spatial_display':'Vortex: linear interpolation for full fields; observations are measured points only. Jet: native (u,v) arrows in |z|<5 slab; no spatial interpolation; same thinned locations for reference and RFormer. No temporal interpolation.','field_limits':limits.tolist(),'arrow_scale':.08 if case=='jet' else None,'slurm_job':os.environ['SLURM_JOB_ID']}
    (OUT/f'{case}.json').write_text(json.dumps(meta,indent=2)+'\n')
    publish(case,meta,lambda path:OUT/Path(path).name)
    with open(f'/tmp/{os.environ["USER"]}.agent-lock','a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        fallback=ROOT/f'public/fallback_figures/ch06/{case}.png';fallback.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(OUT/Path(entries[0]['path']).name,fallback)
    print(case, len(entries), times.tolist(), flush=True)
