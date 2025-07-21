#!/bin/bash
#SBATCH --time=01:00:00
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:1
#SBATCH --mem=16G
#SBATCH --job-name=create_edu_test
#SBATCH --output=class_create_edu_test.out
#SBATCH --error=error_create_edu_test.out
#SBATCH --account=rrg-mageed
#SBATCH --mail-user=rrs99@cs.ubc.ca
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
module load cuda cudnn
source /scratch/rrs99/venv/discourse_parser_venv/bin/activate

python run.py --segment --input_files ../data/results/train1329.out --result_dir ../data/results/

