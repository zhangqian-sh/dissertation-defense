#!/usr/bin/env python3
"""Collect published plot inputs without loading experiment tensors or models.

Run from any directory. Generated inventory is a source-audit snapshot, not a
declaration that every thesis figure has been selected for the final slides.
Existing files with different contents are rejected rather than overwritten.
"""
import csv
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
THESIS = ROOT.parent / 'thesis'


def save(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() != content:
        raise RuntimeError(f'Refusing to replace changed collection: {path}')
    if not path.exists():
        path.write_bytes(content)


def relative(path):
    return str(path.relative_to(ROOT))


def main():
    rows = []
    sources = sorted(THESIS.glob('chapters/*/chapter.tex'))
    sources += [THESIS / 'appendices/app-b-reconstruction-details.tex']
    for source in sources:
        chapter = source.parent.name[:4] if source.name == 'chapter.tex' else 'app-b'
        content = source.read_text()
        for match in re.finditer(r'\\begin\{(figure|table)\}(?:\[[^\]]*\])?(.*?)\\end\{\1\}', content, re.S):
            kind, block = match.groups()
            labels = re.findall(r'\\label\{([^}]+)\}', block)
            if not labels:
                continue
            label = labels[-1]
            slug = label.replace(':', '-')
            folder = ROOT / 'figure_sources' / chapter / slug
            save(folder / 'source.tex', (match.group(0) + '\n').encode())
            inputs, outputs, hashes, missing = [], [], {}, []
            for name in re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}', block):
                path = THESIS / 'images' / name
                if not path.is_file():
                    missing.append(str(path))
                    continue
                inputs.append(str(path))
                hashes[name] = hashlib.sha256(path.read_bytes()).hexdigest()
                if path.suffix.lower() in {'.png', '.jpg', '.jpeg', '.svg'}:
                    target = ROOT / 'public/figures' / chapter / path.name
                    save(target, path.read_bytes())
                    outputs.append(relative(target))
                else:
                    # Original PDFs remain read-only thesis inputs until conversion.
                    outputs.append('pending browser conversion: ' + name)
            metadata = dict(thesis_source=str(source), source_label=label,
                            source_line=content[:match.start()].count('\n') + 1,
                            source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                            image_sha256=hashes, evidence='published thesis artifact',
                            review='Caption retained verbatim; slide selection and visual review pending.')
            save(folder / 'provenance.json', (json.dumps(metadata, indent=2) + '\n').encode())
            rows.append(dict(asset_id=slug, chapter_slide=chapter + '/candidate', treatment='static',
                scientific_question='See retained source caption; final slide selection pending',
                thesis_label=label, input_path=';'.join(inputs) or str(source),
                output_path=';'.join(outputs) or relative(folder / 'source.tex'),
                source_identity=f'{source}:{metadata["source_line"]}',
                processing_command='python scripts/collect_thesis_sources.py',
                collection_status='unavailable' if missing else 'needs_adaptation' if kind == 'table' or not outputs or any(x.startswith('pending') for x in outputs) else 'located',
                dataset_sample_split='See source.tex and chapter; not independently audited',
                normalization='Not independently audited', observation_protocol='See retained caption',
                smoothing='See retained caption; not independently audited',
                metric_units_aggregation='See retained caption; not independently audited', platform='Not independently audited',
                available_fields='Original LaTeX block; provenance; ' + str(len(inputs)) + ' image sources',
                missing_inputs=';'.join(missing), fallback_source=str(source),
                validation_result='Source paths and checksums verified; scientific and visual review pending',
                conditional_evidence='', conditional_decision='', conditional_reason=''))
    for chapter, asset, label, gap in [
        ('ch02', 'sms_sdon', 'fig:snn:ode-vdp', 'Aligned reference/one-step/cascade, physical time, errors, training boundary and selected T captures'),
        ('ch03', 'conversion_over_t', 'ch:conversion-hardware', 'Final-layer emitted spike capture, ANN/reference, calibrated run identity and prefix validation'),
        ('ch07', 'drone_swarm_3d', 'ch:ocformer', 'Selected 3D trajectory, original constraint geometry, clearance traces and exact critical events'),
    ]:
        rows.append(dict(asset_id=asset, chapter_slide=chapter, treatment='required-dynamic',
                         thesis_label=label, collection_status='needs_export', missing_inputs=gap,
                         validation_result='Candidate repositories located; no complete capture validated',
                         output_path=f'data/raw/{chapter}/{asset}/runs/'))
    target = ROOT / 'docs/data_inventory.csv'
    if target.exists():
        raise RuntimeError('Inventory exists; review it before regenerating to preserve manual annotations')
    with target.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f'Collected {len(rows) - 3} static source records; recorded 3 pending dynamic captures.')


if __name__ == '__main__':
    main()
