#!/bin/bash
#SBATCH --job-name=vortex-frame-crop
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=6G
#SBATCH --time=00:10:00
#SBATCH --output=data/staging/vortex-crop-%j.out
#SBATCH --error=data/staging/vortex-crop-%j.err
set -euo pipefail
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2
export RFORMER_CASE=vortex
export RFORMER_OUTPUT="$PWD/data/staging/vortex-crop-$SLURM_JOB_ID"
srun /users/qzhang64/Projects/OperatorLearning/RFormer/.venv/bin/python scripts/export_rformer_time.py
# The exporter publishes the validated bundle and first-frame fallback.
