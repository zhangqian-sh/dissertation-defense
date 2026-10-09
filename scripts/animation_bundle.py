"""Lossless PNG sequence packaging; exporters render into staging first."""
import copy, hashlib, json, os, shutil, fcntl
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def digest(path):
    with open(path,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def images(meta):
    for frame in meta['frames']:
        yield from frame.get('panels',[frame])
def publish(name,metadata,resolve_image):
    meta=copy.deepcopy(metadata)
    stage=ROOT/'data/staging/animation-bundles'/os.environ.get('SLURM_JOB_ID','local')/name
    stage.mkdir(parents=True,exist_ok=True)
    bundle=stage/'frames.bin'; offset=0
    with bundle.open('wb') as target:
        for entry in images(meta):
            source=resolve_image(entry['path']); raw=Path(source).read_bytes()
            assert raw.startswith(b'\x89PNG\r\n\x1a\n'),source
            assert hashlib.sha256(raw).hexdigest()==entry['sha256'],source
            target.write(raw);entry.pop('path')
            entry.update(offset=offset,length=len(raw));offset+=len(raw)
    meta['bundle']={'format':'png-concat-v1','path':f'/data/animations/{name}/frames.bin','byte_length':offset,'sha256':digest(bundle)}
    meta['schema_version']=1
    (stage/'index.json').write_text(json.dumps(meta,indent=2)+'\n')
    # Validate all slices before publication, including their original PNG hashes.
    with bundle.open('rb') as f:
        for entry in images(meta):
            f.seek(entry['offset']);assert hashlib.sha256(f.read(entry['length'])).hexdigest()==entry['sha256']
    with open(f'/tmp/{os.environ["USER"]}.agent-lock','a') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX)
        dest=ROOT/'public/data/animations'/name;dest.mkdir(parents=True,exist_ok=True)
        for filename in ['frames.bin','index.json']:
            temp=dest/(filename+'.tmp');shutil.copyfile(stage/filename,temp);temp.replace(dest/filename)
    return meta
