#!/bin/bash
#PBS -q qprod
#PBS -N <NAME>
#PBS -l select=<NODES>:ncpus=24:mpiprocs=24:accelerator=True:naccelerators=2:accelerator_model=phi7120,walltime=<WALLTIME> 
#PBS -A DD-15-41

cd $PBS_O_WORKDIR
export NODES=<NODES>

module load intel/2016.01
source /scratch/work/user/louhivuo/lib-2016.01/load.sh

(( ncores = NODES * 24 ))
ppn=24

export OMP_NUM_THREADS=1

unset I_MPI_PMI_LIBRARY
export I_MPI_FABRICS=shm:dapl
export I_MPI_DAPL_PROVIDER_LIST=ofa-v2-mlx4_0-1u,ofa-v2-scif0,ofa-v2-mcm-1

GPAW_PPN=$ppn GPAW_OFFLOAD=1 mpirun -np $ncores ./affinity-wrapper.sh $ppn gpaw-python copper-filament.py 

