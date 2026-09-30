#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[4]/'scripts'))
from collection_common import capture
import h5py
import numpy as np
import json


def adapter(args, cfg):
    folder = args.source_root/cfg['source']
    with h5py.File(folder/'analysis/snn_traces.h5') as f:
        layer = f['branch/layer_names'][-1].decode()
        sample = int(f['branch/sample_axis'][0])
        spikes = f['branch/'+layer+'/spikes'][0]
        steps = f['branch/time_axis'][:]
    assert spikes.shape == (cfg['T'],24)
    np.testing.assert_array_equal(steps,np.arange(cfg['T']))
    with np.load(folder/'predictions/snn_predictions.npz', allow_pickle=False) as snn, np.load(folder/'predictions/ann_predictions.npz', allow_pickle=False) as ann:
        index = int(np.flatnonzero(snn['sample_indices']==sample)[0])
        np.testing.assert_array_equal(snn['sample_indices'],ann['sample_indices'])
        normalized = snn['branch_output_normalized'][index]
        np.testing.assert_allclose(spikes.astype(float).mean(0),normalized,rtol=2e-5,atol=2e-6)
        basis=snn['trunk_output'].copy()
        output=snn['y_pred'][index].copy()
        ann_output=ann['y_pred'][index].copy()
        truth=snn['y_true'][index].copy()
        np.testing.assert_allclose(truth,ann['y_true'][index],atol=0,rtol=0)
    with h5py.File(folder/'data/helmholtz_2d_data.h5') as f:
        train=f['train_indices'][:]
        assert sample in f['test_indices'][:] and sample not in train
        # Recover the fixed POD mean from the documented training split, no basis fitting.
        mean=f['y'][np.sort(train)].mean(0)
        coordinates=f['x_trunk'][:]
        cells=f['mesh_cells'][:]
        np.testing.assert_allclose(truth,f['y'][sample],atol=0,rtol=0)
    summary=json.loads((folder/'analysis/pod_summary.json').read_text())
    scales=np.asarray(summary['coefficient_scales'])
    recomposed=mean+(normalized*scales)@basis.T
    np.testing.assert_allclose(recomposed,output,rtol=2e-5,atol=2e-7)
    repo=args.code_root/'SpikingNN/UNO'
    files=[folder/n for n in ['analysis/snn_traces.h5','analysis/pod_summary.json','predictions/ann_predictions.npz','predictions/snn_predictions.npz','data/helmholtz_2d_data.h5','resolved_config.yaml','run_metadata.json','analysis/conversion_state.json']]
    files += [repo/'examples/conversion_deeponet/common'/n for n in ['eval.py','models.py']]
    return dict(step_spikes=spikes,loop_step=steps,returned_subnet_output=normalized,
        returned_field_output=output,ann_output=ann_output,numerical_reference=truth,
        pod_basis=basis,pod_mean=mean,coefficient_scales=scales,coordinates=coordinates,mesh_cells=cells), dict(
        thesis_refs=cfg['thesis_refs'], evidence_status='exploratory',
        evidence_note='Saved documented evaluation of a calibrated Helmholtz POD case; not asserted to reproduce a specific thesis numerical table.',
        sample_ids=[sample],split='held-out test split; seed 2024; 2500 training / 500 test samples',
        seed={'dataset':2024,'conversion':0}, normalization={'coefficients':'training standard deviation','field':'POD mean plus physical coefficients times fixed basis'},
        units={'loop_step':'internal SNN loop index; not physical time','field':'benchmark solution unit','coordinates':'benchmark length unit'},
        protocol=cfg['protocol'],subnet='branch',final_layer=layer,
        prefix_validation={'subnet_max_abs_error':float(np.max(np.abs(spikes.astype(float).mean(0)-normalized))), 'field_max_abs_error':float(np.max(np.abs(recomposed-output)))},
        source_run_metadata=json.loads((folder/'run_metadata.json').read_text()),
        observation_protocol='Saved forward-hook emitted outputs; one sample, all 64 internal steps; fixed POD trunk.',smoothing='none'), files, repo


if __name__ == '__main__':
    capture(__file__, adapter)
