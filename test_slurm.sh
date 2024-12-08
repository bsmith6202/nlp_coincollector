#!/bin/bash
#
#SBATCH --partition=p_nlp
#SBATCH --job-name=test-openai
#SBATCH --output=/nlp/data/andrz/logs/%j.%x.log
#SBATCH --error=/nlp/data/andrz/logs/%j.%x.log
#SBATCH --time=7-0
#SBATCH -c 16
#SBATCH --mem=128G
#SBATCH --gpus=3
#SBATCH --constraint=48GBgpu

srun python3 TextWorldExpress/ask_openai.py "How do trees grow?"