#!/bin/bash
#SBATCH --job-name=defense-figures
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=6G
#SBATCH --time=00:20:00
#SBATCH --output=data/staging/deck-revise-%j.out
#SBATCH --error=data/staging/deck-revise-%j.err
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=2
presentation_python=/users/qzhang64/Projects/OptimalControl/OCFormer/.venv/bin/python
srun "$presentation_python" scripts/prepare_sequence_fallbacks.py
# Current Burgers and vortex-street collectors generate their own fallbacks.
srun "$presentation_python" scripts/prepare_et_contrast.py
srun "$presentation_python" scripts/validate_defense_assets.py public/data/manifest.json
srun "$presentation_python" -m unittest discover -s tests -v
srun node --test tests/field_raster.test.mjs
srun npm run build
srun npm run export:pdf
srun "$presentation_python" scripts/contact_sheets.py --pdf
