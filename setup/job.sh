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

# setup run environment (e.g. load some modules)
#source /path/to/load.sh
module load gpaw-mic

# no. of MPI tasks per node
ppn=12
# no. of MPI tasks in total
(( ncores = SLURM_NNODES * ppn ))
# no. of threads (i.e. no threading)
export OMP_NUM_THREADS=1

# add any system specific configs
unset I_MPI_PMI_LIBRARY
export I_MPI_FABRICS=shm:dapl
export I_MPI_DAPL_PROVIDER=ofa-v2-mlx4_0-1

# bootstrap if in SLURM
bootstrap='-bootstrap slurm'

# if needed, change to working directory first (e.g. in PBS)
#cd $PBS_O_WORKDIR

# launch GPAW
GPAW_PPN=$ppn GPAW_OFFLOAD=1 mpirun -np $ncores $bootstrap ./affinity-wrapper.sh $ppn gpaw-python input.py

