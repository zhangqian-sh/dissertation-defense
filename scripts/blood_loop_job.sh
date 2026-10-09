#!/bin/bash
#SBATCH --job-name=blood-slide-loop
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=12G
#SBATCH --time=00:20:00
#SBATCH --output=data/staging/blood-loop-%j.out
#SBATCH --error=data/staging/blood-loop-%j.err
set -euo pipefail
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=2
srun /users/qzhang64/Projects/OperatorLearning/RFormer/.venv/bin/python scripts/export_blood_loop.py
