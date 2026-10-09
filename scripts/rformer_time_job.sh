#!/bin/bash
#SBATCH --job-name=defense-rformer-time
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=6G
#SBATCH --time=00:20:00
#SBATCH --output=data/staging/rformer-time-%j.out
#SBATCH --error=data/staging/rformer-time-%j.err
set -euo pipefail
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=2
srun /users/qzhang64/Projects/OptimalControl/OCFormer/.venv/bin/python scripts/export_rformer_time.py
