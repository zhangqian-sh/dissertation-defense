"""Shared immutable raw-capture plumbing. No model environments are imported."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
from datetime import datetime, timezone
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = Path('/users/qzhang64/data/qzhang64/Projects')
CODE = Path('/users/qzhang64/Projects')


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def git(repo, *args):
    return subprocess.check_output(['git', '-C', str(repo), *args], text=True).strip()


def capture(package, adapter):
    parser = argparse.ArgumentParser()
    parser.add_argument('--case-id', required=True)
    parser.add_argument('--run-id', required=True)
    parser.add_argument('--source-root', type=Path, default=DATA)
    parser.add_argument('--code-root', type=Path, default=CODE)
    args = parser.parse_args()
    for value in [args.case_id, args.run_id]:
        if not re.fullmatch(r'[A-Za-z0-9_-]+', value):
            raise ValueError('Unsafe case/run ID')
    package = Path(package).resolve().parent
    index = json.loads((package/'runs.yaml').read_text())  # JSON is also valid YAML.
    config = next(r for r in index['runs'] if r['case_id'] == args.case_id and r['run_id'] == args.run_id)
    target = package/'runs'/args.case_id/args.run_id
    if target.exists():
        raise FileExistsError(f'Immutable capture exists: {target}')
    if not os.environ.get('SLURM_JOB_ID'):
        raise RuntimeError('Run the collector inside a Slurm allocation')
    arrays, details, files, repo = adapter(args, config)
    for key, value in arrays.items():
        value = np.asarray(value)
        if value.dtype.kind not in 'biuf' or not np.isfinite(value).all():
            raise ValueError(f'Invalid raw tensor {key}')
        arrays[key] = value
    metadata = dict(schema_version=2, case_id=args.case_id, run_id=args.run_id,
        generated_at=datetime.now(timezone.utc).isoformat(), source_repository=str(repo.resolve()),
        source_commit=git(repo, 'rev-parse', 'HEAD'),
        source_dirty_state=git(repo, 'status', '--porcelain', '--untracked-files=no'),
        historical_training_commit=None,
        provenance_note='Current source identity records the audited reader/definitions, not a recovered training commit.',
        input_files=[dict(path=str(p.resolve()), sha256=digest(p)) for p in files],
        configuration=config, configuration_sha256=digest(package/'runs.yaml'),
        checkpoint_sha256=None, checkpoint_note='Saved outputs reused; no checkpoint loaded or inference executed.',
        environment=dict(interpreter=sys.executable, python=platform.python_version(), numpy=np.__version__),
        slurm={k:v for k,v in os.environ.items() if k.startswith('SLURM_')},
        command=sys.argv, shapes={k:list(v.shape) for k,v in arrays.items()}, **details)
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(target.name + '.partial-' + os.environ['SLURM_JOB_ID'])
    temporary.mkdir()
    np.savez_compressed(temporary/'payload.npz', **arrays)
    metadata['payload_sha256'] = digest(temporary/'payload.npz')
    (temporary/'metadata.json').write_text(json.dumps(metadata, indent=2)+'\n')
    temporary.rename(target)
    print(f'Complete capture: {target}', flush=True)
