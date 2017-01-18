#!/bin/bash
#SBATCH -J knc-test
#SBATCH -p mic
#SBATCH -N 8
#SBATCH -n 96
#SBATCH --ntasks-per-node=12
#SBATCH --cpus-per-task=1
#SBATCH --mem=32000
#SBATCH --time=00:30:00
#SBATCH --gres=mic:2

# if needed, change to working directory first (e.g. in PBS)
#cd $PBS_O_WORKDIR

# read machine specific settings (e.g. hardware topology)
#   (see specs.taito for a SLURM example
#    and specs.salomon for a PBS example)
source specs.taito

# no. of CPU cores per node
ppn=$(( HOST_PE * HOST_CORES ))
# no. of CPU cores in total
cores=$(( NODES * ppn ))

# no. of threads (i.e. no threading)
export OMP_NUM_THREADS=1
# bootstrap if in SLURM
bootstrap='-bootstrap slurm'

# launch GPAW
GPAW_PPN=$ppn GPAW_OFFLOAD=1 mpirun -np $cores $bootstrap ./affinity-wrapper.sh gpaw-python input.py

