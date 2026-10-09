#!/bin/bash
#SBATCH --job-name=blood-slide-redraw
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=6G
#SBATCH --time=00:10:00
#SBATCH --output=data/staging/blood-redraw-%j.out
#SBATCH --error=data/staging/blood-redraw-%j.err
set -euo pipefail
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2
srun /users/qzhang64/Projects/OperatorLearning/RFormer/.venv/bin/python scripts/redraw_blood_snapshot.py
