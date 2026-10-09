#!/bin/bash
#SBATCH --job-name=pack-slide-animations
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --time=00:10:00
#SBATCH --output=data/staging/pack-animations-%j.out
#SBATCH --error=data/staging/pack-animations-%j.err
set -euo pipefail
srun python scripts/pack_animations.py
