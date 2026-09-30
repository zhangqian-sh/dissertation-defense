"""Convert thesis PDF figures into local browser assets; retain source hashes."""
import hashlib
import json
from pathlib import Path
import subprocess
import os
ROOT=Path(__file__).resolve().parents[1]
if not os.environ.get('SLURM_JOB_ID'): raise RuntimeError('Run figure conversion in Slurm')
records=[]
for chapter in ['ch03','ch05','ch06','ch07']:
    target=ROOT/'public/figures'/chapter; target.mkdir(parents=True,exist_ok=True)
    for p in sorted((ROOT.parent/'thesis/images'/chapter).glob('*.pdf')):
        dest=target/(p.stem+'.png')
        if not dest.exists():
            subprocess.run(['pdftocairo','-png','-singlefile','-scale-to','1800',str(p),str(dest.with_suffix(''))],check=True)
        records.append(dict(source=str(p),source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),output=str(dest.relative_to(ROOT)),output_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),command='pdftocairo -png -singlefile -scale-to 1800',review='Source figure converted without cropping or relabeling'))
(ROOT/'docs/figure_conversions.json').write_text(json.dumps(records,indent=2)+'\n')
print(f'Prepared {len(records)} PDF figures')
