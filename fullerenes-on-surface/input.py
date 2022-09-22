###
### GPAW benchmark: Carbon Fullerenes on a Lead Surface
###

from __future__ import print_function
from gpaw.mpi import size, rank
from gpaw import GPAW, Mixer, ConvergenceError
from gpaw.occupations import FermiDirac
from ase.io import read

# grid spacing (decrease to scale up the system)
h = 0.22
# no. of k-points in Brillouin-zone sampling grid (an increase will lift
#   the upper scaling limit, but also consume more memory and time)
kpts = (2,2,1)
# other parameters
input_coords = 'POSCAR'
txt = 'output.txt'
maxiter = 15
parallel = {'sl_default': (4,4,64)}
# uncomment to use GPUs
#gpu = {'cuda': True, 'hybrid_blas': False}

# check which GPU backend (if any) is used
if 'gpu' in locals():
    use_cuda = gpu.get('cuda', False)
else:
    use_cuda = False

# output benchmark parameters
if rank == 0:
    print("#"*60)
    print("GPAW benchmark: Carbon Fullerenes on a Lead Surface")
    print("  grid spacing: h=%f" % h)
    print("  Brillouin-zone sampling: kpts=" + str(kpts))
    print("  MPI tasks: %d" % size)
    print("  using GPU: " + str(use_cuda))
    print("#"*60)
    print("")

# setup parameters
args = {'h': h,
        'nbands': -180,
        'occupations': FermiDirac(0.2),
        'kpts': kpts,
        'xc': 'PBE',
        'mixer': Mixer(0.1, 5, 100),
        'eigensolver': 'rmm-diis',
        'maxiter': maxiter,
        'txt': txt}
if use_cuda:
    args['gpu'] = gpu
    args['xc_thread'] = False
try:
    args['parallel'] = parallel
except: pass

# setup the system
atoms = read(input_coords)
calc = GPAW(**args)
atoms.set_calculator(calc)

# execute the run
try:
    atoms.get_potential_energy()
except ConvergenceError:
    pass

