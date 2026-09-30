#!/bin/bash
#SBATCH --job-name=burgers-prefix
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=00:30:00
#SBATCH --output=data/staging/burgers-prefix-%j.out
#SBATCH --error=data/staging/burgers-prefix-%j.err
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=4
export JAX_PLATFORMS=cpu
export PYTHONPATH=/oscar/data/gk/qzhang64/Applications/venv/pytorch/lib/python3.11/site-packages:/oscar/data/gk/qzhang64/Applications/venv/jax/lib/python3.11/site-packages
srun python3.11 -u data/raw/ch03/burgers_over_t/replay.py
