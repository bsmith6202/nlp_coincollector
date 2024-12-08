#!/bin/bash
#
#SBATCH --partition=p_nlp
#SBATCH --job-name=openai-coin
#SBATCH --output=submit-sslurm-result.txt
#SBATCH --time=7-0
#SBATCH --mem=128G            # Request 128GB of memory
#SBATCH --gpus=3              # Request 3 GPUs
#SBATCH --constraint=48GBgpu  # Request 4 CPUs per task for better performance

srun python kani_mixtral_saving.py