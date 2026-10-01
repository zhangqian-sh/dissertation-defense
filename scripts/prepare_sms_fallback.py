"""Publish the two-panel SMS fallback from unchanged saved browser predictions."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import numpy as np
from export_defense_assets import plot_sms, plt

assert os.environ.get('SLURM_JOB_ID'), 'Run figure preparation in Slurm'
root=Path(__file__).resolve().parents[1]
manifest_path=root/'public/data/manifest.json'
manifest=json.loads(manifest_path.read_text())
entry=next(a for a in manifest['assets'] if a['asset_id']=='ch02/sms_longtime_rollout')
payload=json.loads((manifest_path.parent/entry['path']).read_text())['data']['states'][0]['payload']
def array(key):
    tensor=payload[key]
    return np.asarray(tensor['values']).reshape(tensor['shape'])
arrays={key:array(key) for key in ['time','coordinates','reference_state','one_step_state','cascade_state']}
fig=plot_sms(arrays,payload['training_end_time'],array('one_step_error'),array('cascade_error'))
stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')+'-sms-'+os.environ['SLURM_JOB_ID']
out=manifest_path.parent/'releases'/stamp/'ch02'
out.mkdir(parents=True)
png=out/'sms_longtime_rollout.png'
fig.savefig(png,dpi=160)
plt.close(fig)
shutil.copyfile(png,root/'public/fallback_figures/ch02/sms_longtime_rollout.png')
entry['fallback_path']='/'+png.relative_to(root/'public').as_posix()
entry['fallback_sha256']=hashlib.sha256(png.read_bytes()).hexdigest()
manifest['generated_at']=datetime.now(timezone.utc).isoformat()
manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
print('Published two-panel SMS fallback:',png)
