"""Bounded read-only numerical audit; execute inside Slurm."""
from pathlib import Path
import h5py
import numpy as np
import json

DATA = Path('/users/qzhang64/data/qzhang64/Projects')
sms = DATA / 'SpikingNN/Spiking-Marching-Scheme'
for relative in ['sms_results/heat/heat_0.4', 'review/output/heat/model=2*500_speed=10/output_data/test']:
    folder = sms / relative
    print('SMS', folder, flush=True)
    for name in ['u_true.csv', 'u_pred.csv', 'u_pred_cascade.csv']:
        a = np.loadtxt(folder / name, delimiter=',')
        print(name, a.shape, a.min(), a.max(), a[:3,50], flush=True)
    with np.load(folder / 'u_spikes.npz') as f:
        print('spikes', [(k, f[k].shape) for k in f.files], flush=True)

base = DATA / 'SpikingNN/UNO/examples/conversion_deeponet/helmholtz_2d/final/runs/reverse_conv_v2_calibration_l1_k15_seed2024_T64'
with h5py.File(base/'analysis/snn_traces.h5') as f:
    sample = int(f['branch/sample_axis'][0])
    spikes = f['branch/branch.layer7linear/spikes'][0]
    print('conversion sample', sample, 'spikes', spikes.shape, flush=True)
with np.load(base/'predictions/snn_predictions.npz') as f:
    i = int(np.flatnonzero(f['sample_indices'] == sample)[0])
    print('mean spikes vs normalized branch', np.max(np.abs(spikes.mean(0)-f['branch_output_normalized'][i])), flush=True)
    with h5py.File(base/'data/helmholtz_2d_data.h5') as d:
        mean = d['y'][np.sort(d['train_indices'][:])].mean(0)
    print('POD mean reconstructed error', np.max(np.abs(mean+f['branch_output'][i]@f['trunk_output'].T-f['y_pred'][i])), flush=True)

base = DATA / 'OptimalControl/OCFormer/results/ball_3d/OCFormer_-1_48_l=2e-5'
with h5py.File(base/'best_pred_lbfgs.h5') as f:
    q=f['q'][:].reshape(-1,16,3).astype(float)
    dist=np.linalg.norm(q[:,:,None,:]-q[:,None,:,:],axis=-1)
    i,j=np.triu_indices(16,1)
    print('swarm pair min', (dist[:,i,j]-.04).min(), 'sphere squared min', (np.sum(q*q,axis=-1)-.01+1e-10).min(), flush=True)
