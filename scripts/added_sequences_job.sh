#!/bin/bash
#SBATCH --job-name=defense-added-sequences
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=00:20:00
#SBATCH --output=data/staging/add-sequences-%j.out
#SBATCH --error=data/staging/add-sequences-%j.err
set -euo pipefail
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=2
srun /users/qzhang64/Projects/OperatorLearning/RFormer/.venv/bin/python scripts/export_added_sequences.py
bash scripts/revise_figures_job.sh
