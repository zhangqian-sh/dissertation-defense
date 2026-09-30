#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[4]/'scripts'))
from collection_common import capture
import numpy as np


def adapter(args, cfg):
    folder = args.source_root/cfg['source']
    names = ['u_true.csv', 'u_pred.csv', 'u_pred_cascade.csv', 'u_spikes.npz']
    reference = np.loadtxt(folder/names[0], delimiter=',')
    one = np.loadtxt(folder/names[1], delimiter=',')
    cascade = np.loadtxt(folder/names[2], delimiter=',')
    assert reference.shape == (1001,101), reference.shape
    assert one.shape == cascade.shape == (100,101)
    # Source evaluate() initializes the first two histories at physical indices 0,1.
    indices = np.arange(len(one))*cfg['stride']
    aligned = reference[indices]
    with np.load(folder/'u_spikes.npz', allow_pickle=False) as f:
        spikes = f['pred']; recursive = f['pred_cascade']
    assert spikes.shape == recursive.shape == (100,100,101)
    lo, hi = reference.min(), reference.max()
    np.testing.assert_allclose(lo, 0, atol=1e-10)
    np.testing.assert_allclose(hi, 1, atol=1e-7)
    for emitted, decoded in [(spikes,one),(recursive,cascade)]:
        np.testing.assert_allclose(lo+(np.count_nonzero(emitted,axis=1)+.5)*(hi-lo)/cfg['K'], decoded, atol=1e-7)
    # Validate reference recurrence against source FDM, including its endpoint convention.
    expected = .2*reference[:-1]
    expected[:,1:] += .4*reference[:-1,:-1]
    expected[:,:-1] += .4*reference[:-1,1:]
    np.testing.assert_allclose(reference[1:], expected, rtol=1e-5, atol=1e-7)
    repo = args.code_root/'SpikingNN/spiking_marching_scheme'
    files = [folder/n for n in names] + [repo/'src'/n for n in ['evaluate.py','encoder.py','data_sampler.py','dataset/pde/heat_fdm.py']]
    files += [args.source_root/'SpikingNN/Spiking-Marching-Scheme/review/plot/R1C1.ipynb']
    return dict(reference_state=aligned, one_step_state=one, cascade_state=cascade,
                time=indices*cfg['reference_dt'], coordinates=np.linspace(0,1,101),
                reference_indices=indices, one_step_spikes=spikes, cascade_spikes=recursive), dict(
        thesis_refs=cfg['thesis_refs'], evidence_status='tested',
        sample_ids=['triangular_initial_profile'], split='same initial condition; training then temporal extrapolation',
        normalization={'minimum':float(lo),'maximum':float(hi),'decode':'min+(nonzero_count+0.5)*(max-min)/K'},
        units={'time':'s','coordinates':'benchmark length unit','state':'benchmark temperature unit'},
        observation_protocol='Reference-fed two-history prediction versus recursively fed two-history prediction; first two frames initialized from encoded reference.',
        smoothing='none',
        alignment='reference[0:1000:10]; includes initialized frames; last displayed t=0.0396 s',
        training_boundary_note='Thesis first 80 retained snapshots / 20 extrapolation; source two-history training target last index 80 at t=0.032.',
        source_qualification='R1C1 notebook explicitly locates this run. Current heat solver has 1000 steps; Git HEAD has 10000. Saved 1001-row reference matches thesis horizon. Solver endpoint stencil is retained, not silently changed to clamped zero endpoints.',
        selected_T_note='Independent codec evaluations of the same reference field, illustrative encoding demonstration; not retrained SMS configurations.'), files, repo


if __name__ == '__main__':
    capture(__file__, adapter)
