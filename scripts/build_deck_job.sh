#!/bin/bash
#SBATCH --job-name=defense-build
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=6G
#SBATCH --time=00:20:00
#SBATCH --output=data/staging/deck-build-%j.out
#SBATCH --error=data/staging/deck-build-%j.err

set -euo pipefail
srun npm run build
srun npm run export:pdf
