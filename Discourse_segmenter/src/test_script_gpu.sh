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
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END
module load cuda cudnn
source /home/rrs99/projects/rrg-mageed/rrs99/venvs/tf_4_multitask/bin/activate

export INPUT_DIR=/home/rrs99/projects/rrg-mageed/rrs99/code/NeuralEDUSeg-master/data/fnc_claim_with_articles_only.p
export RESULTS_DIR=/home/rrs99/projects/rrg-mageed/rrs99/code/NeuralEDUSeg-master/output

python3 run.py --segment \
        --input_files=$INPUT_DIR \
        --result_dir=$RESULTS_DIR \


