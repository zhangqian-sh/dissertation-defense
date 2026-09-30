#!/usr/bin/env python3
"""Export validated schema-v2 states from immutable raw captures.

Run in Slurm. A timestamped release is immutable; manifest is replaced last.
Earlier release directories remain available for rollback.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import os
import shutil
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from collection_common import ROOT, digest, git

SPECS = {
    'sms_sdon': ('ch02','SMSRollout','sms_longtime_rollout','heat_triangular','saved_K100'),
    'conversion_over_t': ('ch03','ConversionOverT','conversion_over_t','helmholtz_l1_k15','saved_T064_prefix'),
    'drone_swarm_3d': ('ch07','DroneSwarm3D','ocformer_swarm_3d','ball_3d_M16','saved_lbfgs'),
}


def tensor(array):
    array=np.ascontiguousarray(array)
    assert np.isfinite(array).all()
    return dict(dtype=str(array.dtype),shape=list(array.shape),order='C',values=array.ravel().tolist())


def relative_error(values,reference):
    denominator=np.linalg.norm(reference,axis=-1)
    if np.any(denominator==0):
        raise ValueError('Relative error denominator is zero')
    return np.linalg.norm(values-reference,axis=-1)/denominator


def sms(a,m):
    one_error=relative_error(a['one_step_state'],a['reference_state'])
    cascade_error=relative_error(a['cascade_state'],a['reference_state'])
    cfg=m['configuration']; levels=np.asarray(cfg['selected_T'])
    lo=m['normalization']['minimum']; hi=m['normalization']['maximum']
    normalized=(a['reference_state']-lo)/(hi-lo)
    # Source codec uses Python float floor division, then midpoint decoding.
    approximations=np.stack([lo+(np.minimum(normalized//(1/int(T)),T)+.5)*(hi-lo)/T for T in levels])
    p={k:tensor(a[k]) for k in ['time','reference_state','one_step_state','cascade_state','coordinates']}
    p.update(one_step_error=tensor(one_error),cascade_error=tensor(cascade_error),
             training_end_time=cfg['training_end_time'],encoding_horizon_steps=cfg['K'],
             axes=['physical_time','space'],initialized_frame_count=2,
             error_definition='Unsmoothed relative discrete L2 over all 101 spatial nodes, per physical time; initialized frames retained.',
             selected_T=tensor(levels),T_approximation=tensor(approximations),
             T_approximation_axes=['selected_T','physical_time','space'],
             T_approximation_status='illustrative',
             T_approximation_note=m['selected_T_note']+' Source midpoint decoding is retained, including its upper-end overshoot; no convergence claim for learned rollouts.')
    fig,ax=plt.subplots(1,3,figsize=(15,4),layout='constrained')
    for i in [40,90]:
        ax[0].plot(a['coordinates'],a['reference_state'][i],label=f'reference t={a["time"][i]:.4f}')
        ax[0].plot(a['coordinates'],a['cascade_state'][i],'--',label=f'cascade t={a["time"][i]:.4f}')
    ax[0].set(xlabel='x (benchmark units)',ylabel='temperature',title='Heat SMS: saved predictions'); ax[0].legend(fontsize=7)
    ax[1].plot(a['time'],one_error,label='reference-fed'); ax[1].plot(a['time'],cascade_error,label='cascade')
    ax[1].axvline(cfg['training_end_time'],color='k',ls=':',label='training boundary')
    ax[1].set(xlabel='physical time (s)',ylabel='relative L2 error'); ax[1].legend(fontsize=8)
    ax[2].plot(a['coordinates'],a['reference_state'][40],color='k',label='reference')
    for T,v in zip(levels,approximations): ax[2].plot(a['coordinates'],v[40],label=f'codec T={T}')
    ax[2].set(title='Illustrative codec, fixed reference',xlabel='x'); ax[2].legend(fontsize=8)
    return p,fig


def conversion(a,m):
    steps=a['step_spikes'].astype(float)
    prefixes=np.cumsum(steps,axis=0)/np.arange(1,len(steps)+1)[:,None]
    field=a['pod_mean']+(prefixes*a['coefficient_scales'])@a['pod_basis'].T
    np.testing.assert_allclose(prefixes[-1],a['returned_subnet_output'],rtol=2e-5,atol=2e-6)
    np.testing.assert_allclose(field[-1],a['returned_field_output'],rtol=2e-5,atol=2e-7)
    ref_error=relative_error(field,a['numerical_reference'])
    ann_error=relative_error(field,a['ann_output'])
    p={k:tensor(a[k]) for k in ['loop_step','step_spikes','ann_output','numerical_reference','coordinates','mesh_cells','pod_basis','pod_mean','coefficient_scales','returned_subnet_output','returned_field_output']}
    p.update(simulation_length_T=len(steps),sample_ids=m['sample_ids'],subnet=m['subnet'],final_layer=m['final_layer'],
             prefix_output=tensor(prefixes),field_prefix_output=tensor(field),
             reference_error=tensor(ref_error),conversion_error=tensor(ann_error),
             output_axes=['internal_loop_step','POD_coefficient'],field_axes=['internal_loop_step','mesh_node'],
             error_definition='Unweighted relative discrete L2 on all 1600 native mesh nodes; reference and ANN denominators kept separate.',
             composition='field_prefix_output = pod_mean + (prefix_output * coefficient_scales) @ pod_basis.T',
             protocol=m['protocol'])
    fig,ax=plt.subplots(1,3,figsize=(15,4),layout='constrained')
    xy=a['coordinates']
    limits=(min(a['numerical_reference'].min(),field[-1].min()),max(a['numerical_reference'].max(),field[-1].max()))
    for axis,values,title in [(ax[0],a['numerical_reference'],'Numerical reference'),(ax[1],field[-1],'SNN prefix at T=64')]:
        artist=axis.tripcolor(xy[:,0],xy[:,1],a['mesh_cells'],values,shading='gouraud',vmin=limits[0],vmax=limits[1])
        axis.set(title=title,xlabel='x',ylabel='y',aspect='equal'); fig.colorbar(artist,ax=axis)
    ax[2].plot(np.arange(1,len(steps)+1),ref_error,label='vs numerical reference')
    ax[2].plot(np.arange(1,len(steps)+1),ann_error,label='vs ANN')
    ax[2].set(xlabel='internal prefix length',ylabel='relative L2',title='Saved exploratory Helmholtz case'); ax[2].legend(fontsize=8)
    return p,fig


def swarm(a,m):
    q=a['positions'].astype(float); count=q.shape[1]; radius=m['agent_radius']; R=m['obstacle_radius']
    ii,jj=np.triu_indices(count,1)
    distance=np.linalg.norm(q[:,ii]-q[:,jj],axis=-1)
    pair=np.sqrt(distance**2+1e-10)-2*radius
    sphere=np.sum(q*q,axis=-1)-R**2+1e-10
    sphere_distance=np.linalg.norm(q,axis=-1)-R
    traces=[]; events=[]
    for name,values,unit,definition in [('pairwise_margin',pair,'benchmark length unit','sqrt(distance^2+1e-10)-2*agent_radius'),('sphere_constraint',sphere,'benchmark length unit squared','distance_to_origin^2-R^2+1e-10'),('sphere_distance_margin',sphere_distance,'benchmark length unit','distance_to_origin-R (geometric diagnostic)')]:
        trace=values.min(axis=1)
        traces.append(dict(id=name,units=unit,threshold=0,definition=definition,values=tensor(trace)))
        t,j=np.unravel_index(np.argmin(values),values.shape)
        agents=[int(ii[j]),int(jj[j])] if name=='pairwise_margin' else [int(j)]
        events.append(dict(id=name+'-minimum',trace_id=name,time_index=int(t),time=float(a['time'][t]),
                           agent_ids=agents,obstacle_id=None if name=='pairwise_margin' else 'sphere-0',
                           clearance=float(values[t,j]),positions=tensor(q[t,agents])))
    p={k:tensor(a[k]) for k in ['time','positions','agent_ids','boundary']}
    p.update(benchmark=m['benchmark'],regime=m['regime'],dimension=3,agent_radius=radius,radius_convention=m['radius_convention'],
             obstacles=[dict(id='sphere-0',type='sphere',center=[0,0,0],radius=R,convention='agent-center exclusion zone')],
             clearance_traces=traces,critical_events=events,
             sampled_position_feasible=bool(pair.min()>=0 and sphere.min()>=0),
             feasibility_scope='Pairwise and sphere constraints only, on all 200 original saved frames. No continuous-time, speed or boundary feasibility certification.',
             interpolation='display-only; original frames and critical events preserved without thinning')
    fig=plt.figure(figsize=(13,5),layout='constrained'); ax=fig.add_subplot(121,projection='3d'); trace_ax=fig.add_subplot(122)
    for i in range(count): ax.plot(*q[:,i].T,lw=1)
    u=np.linspace(0,2*np.pi,25); v=np.linspace(0,np.pi,15)
    ax.plot_surface(R*np.outer(np.cos(u),np.sin(v)),R*np.outer(np.sin(u),np.sin(v)),R*np.outer(np.ones_like(u),np.cos(v)),alpha=.25,color='gray')
    event=events[0]; pos=q[event['time_index'],event['agent_ids']]
    ax.scatter(*pos.T,color='red',s=45)
    ax.set(title='16 agents: sphere exclusion zone',xlabel='x',ylabel='y',zlabel='z'); ax.set_box_aspect([1,1,1])
    trace_ax.plot(a['time'],pair.min(axis=1),label='pairwise margin')
    trace_ax.plot(a['time'],sphere_distance.min(axis=1),label='sphere distance margin')
    trace_ax.axhline(0,color='k',ls=':'); trace_ax.axvline(event['time'],color='red',ls=':',label='closest pair')
    trace_ax.set(xlabel='time (s)',ylabel='margin (benchmark length units)',title='Sampled position constraints only'); trace_ax.legend()
    trace_ax.text(.04,.48,f"Closest pair: agents {event['agent_ids']}\nt = {event['time']:.6f} s\nmargin = {event['clearance']:.6g}",transform=trace_ax.transAxes,fontsize=9)
    return p,fig


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,default=ROOT/'public/data')
    parser.add_argument('--raw-root',type=Path,default=ROOT/'data/raw')
    parser.add_argument('--assets',nargs='+',choices=list(SPECS),default=list(SPECS))
    args=parser.parse_args()
    if not os.environ.get('SLURM_JOB_ID'): raise RuntimeError('Export in Slurm')
    public=ROOT/'public'; args.out=args.out.resolve()
    args.out.relative_to(public)
    release=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')+'-'+os.environ['SLURM_JOB_ID']
    staging=ROOT/'data/staging'/release; staging.mkdir(parents=True)
    publish=args.out/'releases'/release
    manifest=dict(schema_version=2,presentation_id='thesis-defense',generated_at=datetime.now(timezone.utc).isoformat(),generator_commit=git(ROOT,'rev-parse','HEAD'),generator_dirty_state=git(ROOT,'status','--porcelain','--untracked-files=normal'),generator_files={str(p.relative_to(ROOT)):digest(p) for p in [Path(__file__),ROOT/'scripts/validate_defense_assets.py']},assets=[])
    for plot in args.assets:
        chapter,component,name,case,run=SPECS[plot]
        raw=args.raw_root/chapter/plot/'runs'/case/run
        m=json.loads((raw/'metadata.json').read_text())
        assert digest(raw/'payload.npz')==m['payload_sha256']
        with np.load(raw/'payload.npz',allow_pickle=False) as z: a={k:z[k] for k in z.files}
        payload,fig={'sms_sdon':sms,'conversion_over_t':conversion,'drone_swarm_3d':swarm}[plot](a,m)
        state_id=case+'--'+run; asset_id=chapter+'/'+name
        source=dict(thesis_refs=m['thesis_refs'],raw_collection_path=str(raw.relative_to(ROOT)),raw_sha256=m['payload_sha256'],metadata_sha256=digest(raw/'metadata.json'),source_commit=m['source_commit'],case_id=case,run_id=run,processing='export_defense_assets.py; float64 derived metrics; no thinning or smoothing',qualifications={k:m[k] for k in ['source_qualification','evidence_note','radius_convention','provenance_note'] if k in m})
        envelope=dict(schema_version=2,asset_id=asset_id,chapter=chapter,title=name.replace('_',' '),generated_at=manifest['generated_at'],source=source,units=m['units'],defaults=dict(state_id=state_id),data=dict(states=[dict(id=state_id,case_id=case,run_id=run,status=m['evidence_status'],protocol_id=case+'-'+run,payload=payload)]))
        target=staging/chapter/(name+'.json'); target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(json.dumps(envelope,separators=(',',':'),allow_nan=False)+'\n')
        fallback=staging/chapter/(name+'.png'); fig.savefig(fallback,dpi=150); plt.close(fig)
        manifest['assets'].append(dict(asset_id=asset_id,chapter=chapter,component=component,path=f'releases/{release}/{chapter}/{name}.json',default_state=state_id,fallback_path='/'+str((publish/chapter/fallback.name).relative_to(public)),sha256=digest(target),fallback_sha256=digest(fallback),status='required'))
    # Validate staging with the same public-path structure before publishing.
    from validate_defense_assets import validate_envelope
    for asset in manifest['assets']:
        validate_envelope(json.loads((staging/asset['chapter']/(asset['asset_id'].split('/')[-1]+'.json')).read_text()))
    publish.parent.mkdir(parents=True,exist_ok=True)
    shutil.copytree(staging,publish)
    # The ET replay is independently collected; a core-data refresh must retain it.
    if (args.out/'manifest.json').exists():
        prior=json.loads((args.out/'manifest.json').read_text())
        manifest['assets'].extend(a for a in prior['assets'] if a['asset_id']=='ch05/energy_history')
    temporary=args.out/'manifest.pending.json'; temporary.write_text(json.dumps(manifest,indent=2)+'\n')
    from validate_defense_assets import validate_manifest
    validate_manifest(temporary,require_all=len(args.assets)==3)
    old=args.out/'manifest.json'
    if old.exists(): shutil.copy2(old,args.out/('manifest.previous-'+release+'.json'))
    temporary.replace(old)
    print(f'Published and validated {len(manifest["assets"])} assets: {old}',flush=True)


if __name__=='__main__': main()
