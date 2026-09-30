#!/bin/bash
#SBATCH --job-name=defense-setup
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --time=00:20:00
#SBATCH --output=data/staging/deck-setup-%j.out
#SBATCH --error=data/staging/deck-setup-%j.err

set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
srun python scripts/prepare_figures.py
srun npm install --no-audit --no-fund
srun ./node_modules/.bin/playwright install chromium
