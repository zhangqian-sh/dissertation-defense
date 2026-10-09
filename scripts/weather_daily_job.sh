#!/bin/bash
#SBATCH --job-name=weather-daily-slides
#SBATCH --partition=debug
#SBATCH --qos=debug
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=00:20:00
#SBATCH --output=data/staging/weather-daily-%j.out
#SBATCH --error=data/staging/weather-daily-%j.err
set -euo pipefail
export OPENBLAS_NUM_THREADS=1
export OMP_NUM_THREADS=2
srun /users/qzhang64/Projects/OperatorLearning/RFormer/.venv/bin/python scripts/export_weather_daily.py
