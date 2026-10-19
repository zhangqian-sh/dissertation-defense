#!/usr/bin/env python3
"""Validate v2 browser contracts and numerical relationships, failing closed."""
import argparse
import json
from pathlib import Path
import numpy as np
from collection_common import ROOT, digest


def array(t):
    assert t['order']=='C'
    assert t['dtype'] in ['float32','float64','int32','int64','bool']
    assert all(isinstance(n,int) and n>=0 for n in t['shape'])
    if 'binary_path' in t:
        assert t['dtype']=='float32' and t['byte_order']=='little'
        path=(ROOT/'public'/t['binary_path'].lstrip('/')).resolve();path.relative_to(ROOT/'public')
        assert digest(path)==t['sha256']
        a=np.fromfile(path,dtype='<f4')
    else:
        a=np.asarray(t['values'],dtype=t['dtype'])
    assert a.ndim==1 and a.size==np.prod(t['shape']) and np.isfinite(a).all()
    return a.reshape(t['shape'])


def tensors(value):
    if isinstance(value,dict):
        if 'dtype' in value: array(value)
        else:
            for v in value.values(): tensors(v)
    elif isinstance(value,list):
        for v in value: tensors(v)
    elif isinstance(value,float): assert np.isfinite(value)


def increasing(a):
    assert a.ndim==1 and len(a)>1 and np.all(np.diff(a)>0)


def rel(a,b): return np.linalg.norm(a-b,axis=-1)/np.linalg.norm(b,axis=-1)


def validate_envelope(e):
    assert e['schema_version']==2
    assert e['source']['thesis_refs'] and e['units']
    assert len(e['source']['raw_sha256'])==64
    tensors(e)
    states=e['data']['states']; ids=[s['id'] for s in states]
    assert len(ids)==len(set(ids)) and e['defaults']['state_id'] in ids
    assert len({(s['case_id'],s['run_id']) for s in states})==len(states)
    for s in states:
        assert s['status'] in ['tested','exploratory','illustrative']
        assert s['case_id'] and s['run_id'] and s['protocol_id']
        p=s['payload']
        if e['chapter']=='ch02':
            t=array(p['time']); increasing(t)
            ref=array(p['reference_state']); one=array(p['one_step_state']); cascade=array(p['cascade_state'])
            assert ref.shape==one.shape==cascade.shape==(len(t),len(array(p['coordinates'])))
            assert t[0]<p['training_end_time']<t[-1]
            assert p['encoding_horizon_steps']>0
            np.testing.assert_allclose(array(p['one_step_error']),rel(one,ref),atol=1e-12)
            np.testing.assert_allclose(array(p['cascade_error']),rel(cascade,ref),atol=1e-12)
            levels=array(p['selected_T']); assert len(levels)>=2 and np.all(levels>0)
            approx=array(p['T_approximation']); assert approx.shape==(len(levels),*ref.shape)
            assert p['T_approximation_status']=='illustrative'
            for n,T in enumerate(levels):
                np.testing.assert_allclose(approx[n],(np.minimum(ref//(1/int(T)),T)+.5)/T,atol=1e-12)
        elif e['chapter']=='ch03' and p.get('benchmark')=='poisson_archived_prefix':
            np.testing.assert_array_equal(array(p['T']),np.arange(1,65))
            frames=array(p['frames']); reference=array(p['reference'])
            assert frames.shape==(64,*reference.shape) and reference.ndim==2
            expected=np.linalg.norm((frames-reference).reshape(64,-1),axis=1)/np.linalg.norm(reference)
            np.testing.assert_allclose(array(p['relative_error']),expected,rtol=2e-6,atol=2e-7)
            assert p['metadata']['calibration_T']==64
            assert p['metadata']['archived_snn_relative_discrepancy']<5e-4
            assert p['metadata']['ann_relative_discrepancy']<1e-5
            assert np.linalg.norm(frames[0]-frames[-1])>0
        elif e['chapter']=='ch03' and p.get('benchmark')=='burgers_fresh_prefix':
            np.testing.assert_array_equal(array(p['T']),np.arange(1,129))
            frames=array(p['frames']);reference=array(p['reference'])
            assert frames.shape==(128,201,300) and reference.shape==(201,300)
            expected=np.linalg.norm((frames-reference).reshape(128,-1),axis=1)/np.linalg.norm(reference)
            np.testing.assert_allclose(array(p['relative_error']),expected,rtol=2e-6)
            assert p['metadata']['calibration_T']==128 and not p['metadata']['archived_calibration_reproduced']
            # Initial silent SNN steps can legitimately decode to the same field.
            assert np.linalg.norm(frames[64]-frames[63])>0 and np.linalg.norm(frames[95]-frames[127])>0
            np.testing.assert_allclose(reference[0],np.sin(array(p['space'])),atol=3e-7)
        elif e['chapter']=='ch03' and p.get('benchmark')=='burgers_1d_spacetime':
            np.testing.assert_array_equal(array(p['T']),[64,128])
            frames=array(p['frames']);reference=array(p['reference']);difference=array(p['difference'])
            assert frames.shape==(2,201,300) and reference.shape==(201,300)
            np.testing.assert_allclose(difference,frames-reference,atol=1e-12)
            np.testing.assert_allclose(array(p['relative_error']),np.linalg.norm(difference.reshape(2,-1),axis=1)/np.linalg.norm(reference),atol=1e-12)
            np.testing.assert_allclose(reference[0],np.sin(array(p['space'])),atol=3e-7)
            np.testing.assert_allclose(reference[:,[0,-1]],0,atol=1e-7)
            increasing(array(p['space']));increasing(array(p['time']))
            assert np.linalg.norm(frames[0]-frames[1])>0
        elif e['chapter']=='ch03':
            step=array(p['loop_step']); np.testing.assert_array_equal(step,np.arange(p['simulation_length_T']))
            spikes=array(p['step_spikes']); prefixes=array(p['prefix_output'])
            assert spikes.shape==prefixes.shape and len(spikes)==len(step)
            np.testing.assert_allclose(prefixes,np.cumsum(spikes.astype(float),axis=0)/np.arange(1,len(step)+1)[:,None],atol=1e-12)
            np.testing.assert_allclose(prefixes[-1],array(p['returned_subnet_output']),rtol=2e-5,atol=2e-6)
            field=array(p['field_prefix_output'])
            np.testing.assert_allclose(field,array(p['pod_mean'])+(prefixes*array(p['coefficient_scales']))@array(p['pod_basis']).T,atol=1e-12)
            np.testing.assert_allclose(field[-1],array(p['returned_field_output']),rtol=2e-5,atol=2e-7)
            np.testing.assert_allclose(array(p['reference_error']),rel(field,array(p['numerical_reference'])),atol=1e-12)
            np.testing.assert_allclose(array(p['conversion_error']),rel(field,array(p['ann_output'])),atol=1e-12)
            assert array(p['coordinates']).shape==(field.shape[1],2)
            cells=array(p['mesh_cells']); assert cells.shape[1]==3 and cells.min()>=0 and cells.max()<field.shape[1]
            assert p['final_layer'] and p['subnet'] and p['sample_ids']
        elif e['chapter']=='ch05':
            t=array(p['iteration']); np.testing.assert_array_equal(t,np.arange(1,13))
            frames=array(p['frames']); reference=array(p['reference'])
            shape=(128,256) if p.get('benchmark')=='vortex_street_2d' else (32,48)
            assert frames.shape==(12,*shape) and reference.shape==shape
            assert array(p['masked']).shape==reference.shape and array(p['energy']).shape==(12,)
            expected=np.linalg.norm((frames-reference).reshape(12,-1),axis=1)/np.linalg.norm(reference)
            np.testing.assert_allclose(array(p['relative_error']),expected,rtol=2e-6)
            assert np.linalg.norm(frames[0]-frames[-1])>0
            assert p['metadata']['final_relative_l2_difference_from_saved']<.01
        elif e['chapter']=='ch07':
            t=array(p['time']); increasing(t); q=array(p['positions']).astype(float); agents=array(p['agent_ids'])
            assert q.shape==(len(t),len(agents),3) and len(set(agents))==len(agents)
            np.testing.assert_array_equal(agents,np.arange(len(agents)))
            obstacle=p['obstacles'][0]; assert obstacle['type']=='sphere' and obstacle['radius']>0
            ii,jj=np.triu_indices(len(agents),1)
            pair=np.sqrt(np.sum((q[:,ii]-q[:,jj])**2,axis=-1)+1e-10)-2*p['agent_radius']
            radius=np.linalg.norm(q-np.asarray(obstacle['center']),axis=-1)
            expected={'pairwise_margin':pair,'sphere_constraint':radius**2-obstacle['radius']**2+1e-10,'sphere_distance_margin':radius-obstacle['radius']}
            traces={v['id']:v for v in p['clearance_traces']}; assert set(traces)==set(expected)
            for key,values in expected.items(): np.testing.assert_allclose(array(traces[key]['values']),values.min(axis=1),atol=1e-12)
            assert len({v['id'] for v in p['critical_events']})==len(expected)
            for event in p['critical_events']:
                values=expected[event['trace_id']]; ti,ci=np.unravel_index(np.argmin(values),values.shape)
                assert ti==event['time_index'] and t[ti]==event['time']
                np.testing.assert_allclose(event['clearance'],values[ti,ci],atol=1e-12)
                expected_agents=[int(ii[ci]),int(jj[ci])] if event['trace_id']=='pairwise_margin' else [int(ci)]
                assert event['agent_ids']==expected_agents
                assert event['obstacle_id']==(None if event['trace_id']=='pairwise_margin' else obstacle['id'])
                np.testing.assert_array_equal(array(event['positions']),q[ti,expected_agents])
            assert p['sampled_position_feasible']==bool(pair.min()>=0 and expected['sphere_constraint'].min()>=0)
        else: raise ValueError('Unsupported chapter schema')


def validate_manifest(path,require_all=True):
    path=Path(path).resolve(); public=ROOT/'public'
    manifest=json.loads(path.read_text()); assert manifest['schema_version']==2
    assets=manifest['assets']; ids=[a['asset_id'] for a in assets]; assert len(ids)==len(set(ids))
    if require_all: assert {'SMSRollout','ConversionOverT','DroneSwarm3D'}<={a['component'] for a in assets}<={'SMSRollout','ConversionOverT','DroneSwarm3D','EnergyHistory','PoissonSpikeDynamics'}
    for a in assets:
        target=(path.parent/a['path']).resolve(); target.relative_to(public)
        fallback=(public/a['fallback_path'].lstrip('/')).resolve(); fallback.relative_to(public)
        assert target.is_file() and fallback.is_file()
        assert digest(target)==a['sha256'] and digest(fallback)==a['fallback_sha256']
        e=json.loads(target.read_text()); assert e['asset_id']==a['asset_id'] and e['chapter']==a['chapter']
        assert e['defaults']['state_id']==a['default_state'] and a['status']=='required'
        raw=(ROOT/e['source']['raw_collection_path']).resolve(); raw.relative_to(ROOT/'data/raw')
        assert digest(raw/'payload.npz')==e['source']['raw_sha256']
        assert digest(raw/'metadata.json')==e['source']['metadata_sha256']
        metadata=json.loads((raw/'metadata.json').read_text())
        schema=json.loads((ROOT/'schemas/raw_capture.schema.json').read_text())
        assert all(k in metadata for k in schema['required'])
        assert metadata['schema_version']==2 and metadata['slurm']['SLURM_JOB_ID']
        assert metadata['payload_sha256']==e['source']['raw_sha256']
        state=e['data']['states'][0]
        assert (state['case_id'],state['run_id'])==(metadata['case_id'],metadata['run_id'])
        with np.load(raw/'payload.npz',allow_pickle=False) as z:
            assert {k:list(z[k].shape) for k in z.files}==metadata['shapes']
            for key in set(z.files).intersection(state['payload']):
                if isinstance(state['payload'][key],dict) and 'dtype' in state['payload'][key]:
                    np.testing.assert_array_equal(z[key],array(state['payload'][key]))
            if state['payload'].get('benchmark') in ['burgers_fresh_prefix','poisson_archived_prefix']:
                frames=np.cumsum(z['step_spikes'].astype(float),axis=0)/np.arange(1,len(z['step_spikes'])+1)[:,None,None]
                np.testing.assert_allclose(frames,z['frames'],rtol=2e-6,atol=2e-7)
        validate_envelope(e)
    print(f'PASS: {len(assets)} assets; tensors, prefixes, errors, events, paths, raw checksums and fallbacks',flush=True)
    return manifest


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('manifest',type=Path)
    args=parser.parse_args(); validate_manifest(args.manifest)
