#!/bin/bash
#SBATCH --time=06:00:00
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:2
#SBATCH --mem=32G
#SBATCH --job-name=parser
#SBATCH --output=class_parser.out
#SBATCH --error=error_parser.out
#SBATCH --account=rrg-mageed
#SBATCH --mail-user=rrs99@cs.ubc.ca
#SBATCH --mail-type=ALL
module load cuda cudnn

source /home/rrs99/projects/def-mageed/rrs99/stagedp_venv/bin/activate

export DATA_DIR=/home/rrs99/scratch/StageDP-master/rfd_complete_1


python3 main.py --eval --eval_dir=$DATA_DIR