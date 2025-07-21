#!/bin/bash
#SBATCH --time=05:00:00
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:2
#SBATCH --mem=32G
#SBATCH --job-name=preprocess
#SBATCH --output=class_preprocess.out
#SBATCH --error=error_preprocess.out
#SBATCH --account=rrg-mageed
#SBATCH --mail-user=rrs99@cs.ubc.ca
#SBATCH --mail-type=ALL
module load cuda cudnn

source /home/rrs99/projects/def-mageed/rrs99/stagedp_venv/bin/activate


export DATA_DIR=/scratch/rrs99/StageDP-master/rfd_complete_1


python3 preprocess.py --data_dir=$DATA_DIR