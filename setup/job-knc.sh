#!/bin/bash
#SBATCH -J knc-test
#SBATCH -p mic
#SBATCH -N 2
#SBATCH -n 24
#SBATCH --ntasks-per-node=12
#SBATCH --cpus-per-task=1
#SBATCH --mem=32000
#SBATCH --time=00:30:00
#SBATCH --gres=mic:2

# read machine specific settings (e.g. hardware topology)
#   (see specs.taito-mic for a SLURM example
#    and specs.salomon for a PBS example)
source specs.taito-mic

# no. of CPU cores per node
ppn=$(( HOST_PE * HOST_CORES ))
# no. of CPU cores in total
cores=$(( NODES * ppn ))

# no. of threads (i.e. no threading)
export OMP_NUM_THREADS=1
# bootstrap if in SLURM
[[ "$QSYSTEM" == "slurm" ]] && bootstrap='-bootstrap slurm'

# if needed, change to working directory first (e.g. in PBS)
[[ "$QSYSTEM" == "pbs" ]] && cd $PBS_O_WORKDIR

# launch GPAW
GPAW_PPN=$ppn GPAW_OFFLOAD=1 mpirun -np $cores $bootstrap ./affinity-wrapper.sh gpaw-python input.py

