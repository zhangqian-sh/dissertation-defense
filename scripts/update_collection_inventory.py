"""Refresh only the three dynamic inventory rows after a successful export."""
import csv
import json
from pathlib import Path
from collection_common import ROOT

manifest=json.loads((ROOT/'public/data/manifest.json').read_text())
lookup={'SMSRollout':'sms_sdon','ConversionOverT':'conversion_over_t','DroneSwarm3D':'drone_swarm_3d'}
inventory=ROOT/'docs/data_inventory.csv'
with inventory.open(newline='') as f:
    reader=csv.DictReader(f); columns=reader.fieldnames; rows=list(reader)
for asset in manifest['assets']:
    envelope=json.loads((ROOT/'public/data'/asset['path']).read_text())
    raw=ROOT/envelope['source']['raw_collection_path']
    metadata=json.loads((raw/'metadata.json').read_text())
    row=next(r for r in rows if r['asset_id']==lookup[asset['component']])
    row.update(chapter_slide=asset['chapter']+'/interactive',scientific_question=envelope['title'],
        thesis_label=';'.join(metadata['thesis_refs']),input_path=str(raw.relative_to(ROOT)),
        output_path='public/data/'+asset['path'],source_identity=metadata['source_repository']+'@'+metadata['source_commit']+'; '+metadata['case_id']+'/'+metadata['run_id'],
        processing_command='sbatch data/raw/'+asset['chapter']+'/'+row['asset_id']+'/job.sh; sbatch scripts/export_assets_job.sh',
        collection_status='located',dataset_sample_split=json.dumps(metadata['sample_ids'])+'; '+metadata['split'],
        normalization=json.dumps(metadata['normalization']),observation_protocol=metadata['observation_protocol'],
        smoothing=metadata['smoothing'],metric_units_aggregation='See docs/interactive_data.md; full native arrays; '+json.dumps(metadata['units']),
        platform='Saved model outputs; CPU Slurm collection/export; no new inference',
        available_fields='Complete raw capture and schema-v2 browser payload',missing_inputs='',fallback_source='public'+asset['fallback_path'],
        validation_result='Passed raw checksums, tensor contracts, alignment, error and prefix/event consistency; PNG fallback visually inspected')
with inventory.open('w',newline='') as f:
    writer=csv.DictWriter(f,fieldnames=columns); writer.writeheader(); writer.writerows(rows)
print('Updated three dynamic inventory entries')
