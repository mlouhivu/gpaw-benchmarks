#!/bin/bash -l
#SBATCH -J cpu-test
#SBATCH -p test
#SBATCH -N 1
#SBATCH --time=00:30:00

# read machine specific settings (e.g. hardware topology)
#   (see specs.sisu for an example)
source specs.sisu

# no. of cores per node
ppn=$(( PE * CORES ))
# no. of cores in total
cores=$(( NODES * ppn ))

# if needed, change to working directory first (e.g. in PBS)
[[ "$QSYSTEM" == "pbs" ]] && cd $PBS_O_WORKDIR

# launch GPAW
aprun -n $cores gpaw-python input.py

