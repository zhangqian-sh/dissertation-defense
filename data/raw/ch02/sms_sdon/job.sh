#!/bin/bash
#SBATCH --job-name=collect-ch02
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --output=data/raw/ch02/sms_sdon/logs/%x-%j.out
#SBATCH --error=data/raw/ch02/sms_sdon/logs/%x-%j.err

set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
srun /users/qzhang64/Projects/OptimalControl/OCFormer/.venv/bin/python data/raw/ch02/sms_sdon/collect.py --case-id heat_triangular --run-id saved_K100 "$@"
