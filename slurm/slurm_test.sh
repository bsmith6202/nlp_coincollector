#!/bin/bash
#
#SBATCH --job-name=test
#SBATCH --output=res.txt
#SBATCH --ntasks=1
#SBATCH --time=10:00
#SBATCH --mem-per-cpu=200

srun hostname
srun python3 TextWorldExpress/ask_openai.py "How do trees grow?"
