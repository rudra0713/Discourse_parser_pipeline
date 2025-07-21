#!/bin/bash
#SBATCH --time=24:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:2
#SBATCH --mem=32G
#SBATCH --job-name=eval_3
#SBATCH --output=eval_3.out
#SBATCH --error=eval_3.out
#SBATCH --account=rrg-mageed
#SBATCH --mail-user=rrs99@cs.ubc.ca
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
module load cuda cudnn
source /home/rrs99/projects/rrg-mageed/rrs99/venvs/b_torch/bin/activate


export DATA_DIR=/home/rrs99/scratch/StageDP-master/My_data_3

python3 main.py --eval --eval_dir=$DATA_DIR
