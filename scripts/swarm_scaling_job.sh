#!/bin/bash
#SBATCH --job-name=swarm-scaling-slides
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:05:00
#SBATCH --output=data/staging/swarm-scaling-%j.out
#SBATCH --error=data/staging/swarm-scaling-%j.err
set -euo pipefail
export OPENBLAS_NUM_THREADS=1
srun /users/qzhang64/Projects/OperatorLearning/RFormer/.venv/bin/python scripts/export_swarm_scaling.py
