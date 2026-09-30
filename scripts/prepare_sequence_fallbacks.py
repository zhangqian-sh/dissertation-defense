"""Copy the same first recorded frame for offline/PDF/failure fallbacks."""
import json,hashlib,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/'public/fallback_figures/sequences';out.mkdir(parents=True,exist_ok=True)
for name in ['latent','swarm128','weather']:
    meta=json.loads((root/f'public/data/sequences/{name}/index.json').read_text())
    first=meta['frames'][0];p=root/'public'/first['path'].lstrip('/')
    assert hashlib.sha256(p.read_bytes()).hexdigest()==first['sha256']
    shutil.copyfile(p,out/f'{name}.png')
