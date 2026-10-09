"""Export four saved 2D antipodal trajectories for native canvas playback (Slurm)."""
import os,json,hashlib,fcntl,shutil
from pathlib import Path
import h5py
import numpy as np
assert os.environ.get('SLURM_JOB_ID'),'Use Slurm'
ROOT=Path(__file__).resolve().parents[1]
SOURCE=Path('/oscar/data/gk/qzhang64/Projects/OptimalControl/OCFormer')
stage=ROOT/'data/staging'/f'swarm-scaling-{os.environ["SLURM_JOB_ID"]}';stage.mkdir(parents=True,exist_ok=True)
def sha(path):
    with open(path,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
meta={'frame_count':200,'times':np.linspace(0,10,200).tolist(),'display_extent':[-.52,.52,-.52,.52],'cases':[],'dtype':'float32','byte_order':'little','slurm_job':os.environ['SLURM_JOB_ID'],'source_protocol':'Saved best_pred_lbfgs q; no inference, temporal interpolation, or smoothing. Radii from thesis tab:oc:2d-scaling. Animation is not the 5000-time clearance evaluation.'}
offset=0
with (stage/'positions.f32').open('wb') as out:
 for agents in [8,16,32,128]:
    source=SOURCE/f'results/room_2d/OCFormer_0_{2*agents}_M={agents}/best_pred_lbfgs.h5'
    boundary=SOURCE/f'data/room_2d/n={agents}/boundary.h5'
    with h5py.File(source) as f:positions=f['q'][:].reshape(200,agents,2).astype('<f4')
    with h5py.File(boundary) as f:ends=f['boundary'][:].reshape(2,agents,2)
    assert np.isfinite(positions).all()
    assert np.max(np.abs(positions[[0,-1]]-ends))<.02
    rng=np.random.default_rng(5);colors=['#%06X'%rng.integers(0,0xFFFFFF) for _ in range(agents)]
    blob=positions.tobytes();out.write(blob)
    meta['cases'].append({'agents':agents,'radius':.01 if agents==128 else .02,'shape':list(positions.shape),'float_offset':offset,'source':str(source),'source_sha256':sha(source),'boundary_source':str(boundary),'boundary_sha256':sha(boundary),'colors':colors})
    offset+=positions.size
meta['binary']={'path':'/data/ch07/swarm-scaling/positions.f32','byte_length':4*offset,'sha256':sha(stage/'positions.f32')}
(stage/'index.json').write_text(json.dumps(meta,indent=2)+'\n')
with open(f'/tmp/{os.environ["USER"]}.agent-lock','a') as lock:
 fcntl.flock(lock,fcntl.LOCK_EX)
 dest=ROOT/'public/data/ch07/swarm-scaling';dest.mkdir(parents=True,exist_ok=True)
 for name in ['positions.f32','index.json']:shutil.copyfile(stage/name,dest/name)
print('Exported',offset,'float32 coordinates for 8/16/32/128 agents.',flush=True)
