#!/bin/bash
#
#SBATCH --partition=p_nlp
#SBATCH --job-name=openai-coin
#SBATCH --output=openai-4omini-batch-10-50-testing.txt
#SBATCH --ntasks=1
#SBATCH --time=7-0
#SBATCH --mem=48G            
#SBATCH --gpus=1              
#SBATCH --constraint=48GBgpu

srun python3 coin_collector_runner.py