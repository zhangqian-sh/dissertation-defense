#!/bin/bash
#SBATCH --job-name=ocformer-examples-slides
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:05:00
#SBATCH --output=data/staging/ocformer-examples-%j.out
#SBATCH --error=data/staging/ocformer-examples-%j.err
set -euo pipefail
export OPENBLAS_NUM_THREADS=1
srun /users/qzhang64/Projects/OperatorLearning/RFormer/.venv/bin/python scripts/export_ocformer_examples.py
