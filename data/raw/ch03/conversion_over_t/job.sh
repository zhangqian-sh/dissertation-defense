#!/bin/bash
#SBATCH --job-name=collect-ch03
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --output=data/raw/ch03/conversion_over_t/logs/%x-%j.out
#SBATCH --error=data/raw/ch03/conversion_over_t/logs/%x-%j.err

set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
srun /users/qzhang64/Projects/OptimalControl/OCFormer/.venv/bin/python data/raw/ch03/conversion_over_t/collect.py --case-id helmholtz_l1_k15 --run-id saved_T064_prefix "$@"
