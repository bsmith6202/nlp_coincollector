#!/bin/bash
#
#SBATCH --partition=p_nlp
#SBATCH --job-name=openai-coin
#SBATCH --output=pddl-15-20trials-jsonformat-4omini.txt
#SBATCH --ntasks=1
#SBATCH --time=7-0
#SBATCH --mem=128G            
#SBATCH --gpus=3              
#SBATCH --constraint=48GBgpu

srun python3 pddl_coin_runner.py