#!/bin/bash
#SBATCH --job-name=hybrid-rformer-slides
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=6G
#SBATCH --time=00:10:00
#SBATCH --output=data/staging/hybrid-rformer-%j.out
#SBATCH --error=data/staging/hybrid-rformer-%j.err
set -euo pipefail
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2
srun /users/qzhang64/Projects/OperatorLearning/RFormer/.venv/bin/python scripts/export_hybrid_rformer_time.py
