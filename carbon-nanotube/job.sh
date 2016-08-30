#!/bin/bash
#SBATCH -J mic-nanotube
#SBATCH -p mic
#SBATCH -N 8
#SBATCH -n 96
#SBATCH --ntasks-per-node=12
#SBATCH --cpus-per-task=1
#SBATCH --mem=32000
#SBATCH --time=120
#SBATCH --gres=mic:2

module purge
module use $USERAPPL/modules

module load intel/15.0.2 mkl/11.2.2 intelmpi/5.0.2
module load ase/svn gpaw-setups/0.9.11271
module load libxc python/2.7.10-icc pymic gpaw-mic

(( ncores = SLURM_NNODES * 12 ))
ppn=12

export OMP_NUM_THREADS=1

unset I_MPI_PMI_LIBRARY
export I_MPI_FABRICS=shm:dapl
export I_MPI_DAPL_PROVIDER=ofa-v2-mlx4_0-1

GPAW_PPN=$ppn GPAW_OFFLOAD=1 mpirun -np $ncores -bootstrap slurm ./affinity-wrapper.sh $ppn gpaw-python input.py

