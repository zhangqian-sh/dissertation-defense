#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[4]/'scripts'))
from collection_common import capture
import h5py
import numpy as np
import yaml


def adapter(args, cfg):
    folder=args.source_root/cfg['source']
    config_path=args.code_root/cfg['config']
    config=yaml.safe_load(config_path.read_text())
    with h5py.File(folder/'best_pred_lbfgs.h5') as f:
        q=f['q'][:]; p=f['p'][:]
    assert q.shape == p.shape == (config['num_t'],48)
    with h5py.File(config['boundary_path']) as f:
        boundary=f['boundary'][:].reshape(2,16,3)
    q=q.reshape(-1,16,3)
    assert np.max(np.abs(q[[0,-1]]-boundary))<.01
    repo=args.code_root/'OptimalControl/OCFormer'
    files=[folder/'best_pred_lbfgs.h5',config_path,Path(config['boundary_path'])]
    files += [repo/'src'/n for n in ['problems.py','run_ball_3d.py','trainer.py']]
    return dict(positions=q,momentum=p.reshape(-1,16,3),boundary=boundary,
                time=np.linspace(0,config['t_terminal'],config['num_t']),agent_ids=np.arange(16)), dict(
        thesis_refs=cfg['thesis_refs'], evidence_status='tested', sample_ids=['ball_3d_M16'],
        split='per-instance optimized trajectory; not amortized held-out evaluation',
        seed=config['seed'],normalization='Native source coordinates; no rescaling',
        units={'time':'s','positions':'benchmark length unit'},
        benchmark='sphere obstacle',regime='per-instance Adam plus L-BFGS',dimension=3,
        original_config=config,agent_radius=.02,obstacle_radius=config.get('ball_radius',.2*config['halfroomsz']),
        radius_convention='Pairwise distance threshold 2*agent_radius. Sphere is a center exclusion zone; do not add agent radius to sphere radius.',
        constraint_definitions={'pairwise':'sqrt(sum((qi-qj)^2)+1e-10)-2*dr','sphere':'sum(qi^2)-R^2+1e-10'},
        time_provenance='trainer.save_trajectories linspace(0,t_terminal,num_t); HDF5 stores q,p without explicit time. Export uses nominal grid in float64.',
        observation_protocol='All 200 saved evaluation frames preserved; sampled position feasibility only. Speed and continuous-time safety are not certified.',
        smoothing='none'),files,repo


if __name__ == '__main__':
    capture(__file__, adapter)
