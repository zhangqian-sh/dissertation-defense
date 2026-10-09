"""Package recorded transfer and 3D trajectories for the two OCFormer slides."""
import os,json,hashlib,fcntl,shutil
from pathlib import Path
import h5py
import numpy as np
assert os.environ.get('SLURM_JOB_ID'), 'Run through Slurm'
ROOT=Path(__file__).resolve().parents[1]
OC=Path('/oscar/data/gk/qzhang64/Projects/OptimalControl/OCFormer')
SF=OC.parent/'sympnet/SympFormer'
stage=ROOT/'data/staging'/f'ocformer-examples-{os.environ["SLURM_JOB_ID"]}'
stage.mkdir(parents=True,exist_ok=True)
def sha(p):
 with open(p,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
specs=[
 ('perturbation-8',SF/'results/circle/n=8/SympFormer_-1_16_perturbation_uniform_all/boundary_0000/best_pred_lbfgs.h5',2,.02),
 ('perturbation-16',SF/'results/circle/n=16/SympFormer_-1_32_perturbation_0.2_uniform_all/boundary_0000/best_pred_lbfgs.h5',2,.02),
 ('perturbation-128',SF/'results/circle/SympFormer_-1_256_perturbation_0.2_uniform_all/boundary_0000/best_pred_lbfgs.h5',2,.01),
 ('perturbation',SF/'results/circle/n=32/SympFormer_-1_64_perturbation_0.2_uniform_all/boundary_0000/best_pred_lbfgs.h5',2,.02),
 ('ball',OC/'results/ball_3d/OCFormer_-1_48_l=2e-5/best_pred_lbfgs.h5',3,.02),
 ('wall',OC/'results/room_3d/positional/OCFormer_-1_300_mean/best_pred_lbfgs.h5',3,.01)]
meta={'frame_count':200,'times':np.linspace(0,10,200).tolist(),'dtype':'float32','byte_order':'little','cases':{},'slurm_job':os.environ['SLURM_JOB_ID'],'protocol':'Recorded q, no temporal interpolation, smoothing, or new inference.'}
offset=0
with (stage/'positions.f32').open('wb') as out:
 for name,source,dim,radius in specs:
  with h5py.File(source) as f:q=f['q'][:].reshape(200,-1,dim).astype('<f4')
  assert np.isfinite(q).all()
  rng=np.random.default_rng(5)
  c={'shape':list(q.shape),'agents':q.shape[1],'dimension':dim,'radius':radius,'float_offset':offset,'source':str(source),'source_sha256':sha(source),'colors':['#%06X'%rng.integers(0,0xFFFFFF) for _ in range(q.shape[1])]}
  if dim==3:
   if name=='ball':
    c['extent']=[[-.55,.55]]*3
    c['barriers']=[]
    c['sphere']={'center':[0,0,0],'radius':.1}
    boundary=OC/'data/ball_3d/n=16/boundary.h5'
    with h5py.File(boundary) as f:ends=f['boundary'][:].reshape(2,16,3)
    assert abs(q[[0,-1]]-ends).max()<.002
    c.update(boundary_source=str(boundary),boundary_sha256=sha(boundary),geometry_source=str(OC/'archive/ocformer/run_3d_ball.py'))
   else:
    c['extent']=[[-.5,.5],[-.5,.5],[0,1]]
    c['barriers']=[[[-.2,.2],[-.05,.05],[0,.7]],[[.2,.4],[-.1,.1],[0,.4]]]
    c['geometry_source']=str(OC/'archive/ocformer/run_3d.py')
  else:
   agents=q.shape[1]
   tag='uniform_all' if agents==8 else '0.2_uniform_all'
   boundary=SF/f'data/circle/n={agents}/boundary_perturb_{tag}_seed=0.h5'
   with h5py.File(boundary) as f:
    ends=f['boundary'][0].reshape(2,agents,2);reference=f['reference'][:].reshape(2,agents,2)
   endpoint_error=float(abs(q[[0,-1]]-ends).max())
   assert endpoint_error<.02
   c.update(endpoint_error_max=endpoint_error,perturbation_variant=tag,boundary=ends.tolist(),reference=reference.tolist(),boundary_source=str(boundary),boundary_sha256=sha(boundary),initial_delta_max=float(abs(ends[0]-reference[0]).max()),terminal_delta_max=float(abs(ends[1]-reference[1]).max()),extent=[[-.6,.6],[-.6,.6]])
  meta['cases'][name]=c
  out.write(q.tobytes());offset+=q.size
meta['binary']={'path':'/data/ch07/ocformer-examples/positions.f32','byte_length':offset*4,'sha256':sha(stage/'positions.f32')}
(stage/'index.json').write_text(json.dumps(meta,indent=2)+'\n')
with open(f'/tmp/{os.environ["USER"]}.agent-lock','a') as lock:
 fcntl.flock(lock,fcntl.LOCK_EX)
 dest=ROOT/'public/data/ch07/ocformer-examples';dest.mkdir(parents=True,exist_ok=True)
 for name in ['positions.f32','index.json']:shutil.copyfile(stage/name,dest/name)
print('Exported',offset*4,'bytes; cases:',list(meta['cases']))
