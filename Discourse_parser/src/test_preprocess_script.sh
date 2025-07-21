#!/bin/bash
#SBATCH --time=22:00:00
#SBATCH --array=1-27
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:2
#SBATCH --mem=32G
#SBATCH --job-name=preprocess
#SBATCH --output=class_preprocess_%a.out
#SBATCH --error=error_preprocess_%a.out
#SBATCH --account=rrg-mageed
#SBATCH --mail-user=rrs99@cs.ubc.ca
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
module load cuda cudnn

source /home/rrs99/projects/rrg-mageed/rrs99/venvs/b_torch/bin/activate


export DATA_DIR=/home/rrs99/scratch/StageDP-master/complete_$SLURM_ARRAY_TASK_ID


python3 preprocess.py --data_dir=$DATA_DIR