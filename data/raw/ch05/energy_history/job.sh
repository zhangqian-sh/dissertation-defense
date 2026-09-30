#!/bin/bash
#SBATCH --job-name=et-history
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=00:15:00
#SBATCH --output=data/staging/et-history-%j.out
#SBATCH --error=data/staging/et-history-%j.err
set -euo pipefail
export JAX_PLATFORMS=cpu
export PYTHONDONTWRITEBYTECODE=1
export OMP_NUM_THREADS=4
# The historical environment's interpreter symlink points to a retired path.
# Reuse its pinned Python 3.11 packages with the available Python 3.11 runtime.
export PYTHONPATH=/oscar/data/gk/qzhang64/Applications/venv/jax/lib/python3.11/site-packages
srun python3.11 data/raw/ch05/energy_history/collect.py
