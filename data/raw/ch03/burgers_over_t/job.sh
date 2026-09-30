#!/bin/bash
#SBATCH --job-name=burgers-plots
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=3G
#SBATCH --time=00:05:00
#SBATCH --output=data/staging/burgers-plots-%j.out
#SBATCH --error=data/staging/burgers-plots-%j.err
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1
srun /users/qzhang64/Projects/OptimalControl/OCFormer/.venv/bin/python data/raw/ch03/burgers_over_t/collect.py
