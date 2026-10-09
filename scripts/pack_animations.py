"""Migrate existing exported PNGs without rerendering (run on Slurm)."""
import json,os,shutil,fcntl
from pathlib import Path
from animation_bundle import ROOT,publish
assert os.environ.get('SLURM_JOB_ID'),'Use Slurm'
indexes={name:ROOT/f'public/data/sequences/{name}/index.json' for name in ['weather','latent','swarm128']}
indexes.update({name:ROOT/f'public/data/ch06/time/{name}.json' for name in ['vortex','jet']})
indexes['blood']=ROOT/'public/data/ch06/blood-loop/index.json'
backup=ROOT/'data/staging/animation-migration'/os.environ['SLURM_JOB_ID'];backup.mkdir(parents=True,exist_ok=True)
for name,index in indexes.items():
    metadata=json.loads(index.read_text())
    packed=publish(name,metadata,lambda path:ROOT/'public'/path.lstrip('/'))
    if name in ['vortex','jet']:
        fallback=ROOT/f'public/fallback_figures/ch06/{name}.png';fallback.parent.mkdir(parents=True,exist_ok=True)
        with open(f'/tmp/{os.environ["USER"]}.agent-lock','a') as lock:
            fcntl.flock(lock,fcntl.LOCK_EX)
            shutil.copyfile(ROOT/'public'/metadata['frames'][0]['path'].lstrip('/'),fallback)
    print(name,len(metadata['frames']),packed['bundle']['byte_length'],flush=True)
# Archive only the superseded indexes/frames, after all six bundles validate.
with open(f'/tmp/{os.environ["USER"]}.agent-lock','a') as lock:
    fcntl.flock(lock,fcntl.LOCK_EX)
    for name,index in indexes.items():
        metadata=json.loads(index.read_text())
        paths=[index]
        for frame in metadata['frames']:
            paths.extend(ROOT/'public'/p['path'].lstrip('/') for p in frame.get('panels',[frame]))
        for source in paths:
            destination=backup/source.relative_to(ROOT/'public');destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.move(str(source),str(destination))
        if index.parent.exists() and not any(index.parent.iterdir()):index.parent.rmdir()
    metrics=ROOT/'public/data/ch06/blood-metrics.json'
    if metrics.exists():shutil.move(str(metrics),str(backup/'blood-metrics.json'))
print('Validated six bundles; original frames archived in',backup,flush=True)
