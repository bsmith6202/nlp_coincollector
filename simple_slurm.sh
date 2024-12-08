#!/bin/bash
#
#SBATCH --partition=p_nlp
#SBATCH --job-name=openai-simple
#SBATCH --output=/nlp/data/andrz/logs/%j.test-openai-simple.log
#SBATCH --error=/nlp/data/andrz/logs/%j.test-openai-simple.log
#SBATCH --time=00:10:00   # Short time limit for testing
#SBATCH --ntasks=1        # Single task
#SBATCH --cpus-per-task=1 # 1 CPU core
#SBATCH --mem=4G          # 4GB memory, adjust as needed

# Print environment variables to log
echo "Environment Variables:" >> /nlp/data/andrz/logs/%j.test-openai-env.log
printenv >> /nlp/data/andrz/logs/%j.test-openai-env.log

# Run the Python script
python3 TextWorldExpress/ask_openai.py "How do trees grow?"