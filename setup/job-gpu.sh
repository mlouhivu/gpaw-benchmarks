#!/bin/bash
#SBATCH -J gpu-test
#SBATCH -p gpu
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
#SBATCH --time=00:30:00
#SBATCH --mem=32000
#SBATCH --gres=gpu:1
#SBATCH --constraint=k80

# read machine specific settings (e.g. hardware topology)
#   (see specs.cartesius for a SLURM example)
source specs.taito-gpu

# if needed, change to working directory first (e.g. in PBS)
[[ "$QSYSTEM" == "pbs" ]] && cd $PBS_O_WORKDIR

# launch GPAW
srun gpaw-python input.py

