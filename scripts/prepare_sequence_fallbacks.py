"""Copy the same first recorded frame for offline/PDF/failure fallbacks."""
import json,hashlib,shutil
from pathlib import Path
root=Path(__file__).resolve().parents[1]
out=root/'public/fallback_figures/sequences';out.mkdir(parents=True,exist_ok=True)
for name in ['latent','swarm128','weather']:
    meta=json.loads((root/f'public/data/animations/{name}/index.json').read_text())
    first=meta['frames'][0];bundle=root/'public'/meta['bundle']['path'].lstrip('/')
    with bundle.open('rb') as f:
        f.seek(first['offset']);raw=f.read(first['length'])
    assert hashlib.sha256(raw).hexdigest()==first['sha256']
    (out/f'{name}.png').write_bytes(raw)
