#!/bin/bash
#PBS -N knl-test
#PBS -j oe
#PBS -l select=1:aoe=quad_100
#PBS -l walltime=00:30:00
#PBS -A your-account

# read machine specific settings (e.g. hardware topology)
#   (see specs.archer for an example)
source specs.archer

# no. of cores per node
ppn=$(( PE * CORES ))
# no. of cores in total
cores=$(( NODES * ppn ))

# no. of threads (i.e. no threading)
export OMP_NUM_THREADS=1
# disable hyperthreading (to enable change e.g. to 2T)
export KMP_HW_SUBSET=1T

# if needed, change to working directory first (e.g. in PBS)
[[ "$QSYSTEM" == "pbs" ]] && cd $PBS_O_WORKDIR

# launch GPAW
aprun -n $cores gpaw-python input.py

