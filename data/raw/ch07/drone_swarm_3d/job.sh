#!/bin/bash
#SBATCH --job-name=collect-ch07
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --output=data/raw/ch07/drone_swarm_3d/logs/%x-%j.out
#SBATCH --error=data/raw/ch07/drone_swarm_3d/logs/%x-%j.err

set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=1
srun /users/qzhang64/Projects/OptimalControl/OCFormer/.venv/bin/python data/raw/ch07/drone_swarm_3d/collect.py --case-id ball_3d_M16 --run-id saved_lbfgs "$@"
