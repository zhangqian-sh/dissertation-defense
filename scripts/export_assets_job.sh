#!/bin/bash
#SBATCH --job-name=defense-export
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --output=data/staging/export-%j.out
#SBATCH --error=data/staging/export-%j.err

set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
export MPLCONFIGDIR="$PWD/data/staging/matplotlib"
srun /users/qzhang64/Projects/OptimalControl/OCFormer/.venv/bin/python scripts/export_defense_assets.py "$@"
srun /users/qzhang64/Projects/OptimalControl/OCFormer/.venv/bin/python -m unittest discover -s tests -v
