#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:2
#SBATCH --mem=32G
#SBATCH --job-name=create_edu
#SBATCH --output=class_create_edu.out
#SBATCH --error=error_create_edu.out
#SBATCH --account=rrg-mageed
#SBATCH --mail-user=rrs99@cs.ubc.ca
#SBATCH --mail-type=ALL
module load cuda cudnn
source /home/rrs99/projects/def-mageed/rrs99/neuraledu_venv/bin/activate

export INPUT_DIR=/scratch/rrs99/Stance_Detection_LST/data/data_stance_rfd/rfd_claim_with_articles_only.p
export RESULTS_DIR=/scratch/rrs99/Stance_Detection_LST/data/data_stance_rfd/
export RESULT_FILE=rfd_claim_with_articles_edus

python3 run.py --segment \
        --input_files=$INPUT_DIR \
        --result_dir=$RESULTS_DIR \
        --result_file=$RESULT_FILE \


python3 run.py --segment --input_files=../data/rfd_claim_with_articles_only.p --result_dir=../data --result_file=rfd_claim_with_articles_edus