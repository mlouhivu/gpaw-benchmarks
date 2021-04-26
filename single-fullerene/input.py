###
### GPAW benchmark: Single Carbon Fullerene
###

from __future__ import print_function
from gpaw.mpi import size, rank
from gpaw import GPAW, Mixer, ConvergenceError
from gpaw.occupations import FermiDirac
from ase.io import read
try:
    from gpaw.eigensolvers.rmm_diis import RMM_DIIS
except ImportError:
    from gpaw.eigensolvers.rmmdiis import RMMDIIS as RMM_DIIS
try:
    from gpaw import use_mic
except ImportError:
    use_mic = False
try:
    from gpaw import use_cuda
    use_cuda = True
except ImportError:
    use_cuda = False
use_cpu = not (use_mic or use_cuda)

# grid spacing (decrease to scale up the system)
h = 0.22
# no. of k-points in Brillouin-zone sampling grid (an increase will lift
#   the upper scaling limit, but also consume more memory and time)
kpts = (2,2,1)
# other parameters
input_coords = 'POSCAR'
txt = 'output.txt'
maxiter = 15
parallel = {'sl_default': (2,2,64)}

# output benchmark parameters
if rank == 0:
    print("#"*60)
    print("GPAW benchmark: Single Carbon Fullerene")
    print("  grid spacing: h=%f" % h)
    print("  Brillouin-zone sampling: kpts=" + str(kpts))
    print("  MPI tasks: %d" % size)
    print("  using CUDA (GPGPU): " + str(use_cuda))
    print("  using pyMIC (KNC) : " + str(use_mic))
    print("  using CPU (or KNL): " + str(use_cpu))
    print("#"*60)
    print("")

# compatibility hack for the eigensolver
rmm = RMM_DIIS(cuda=True)
rmm.niter = 2
# setup parameters
args = {'h': h,
        'nbands': -180,
        'occupations': FermiDirac(0.2),
        'kpts': kpts,
        'xc': 'PBE',
        'mixer': Mixer(0.1, 5, 100),
        'eigensolver': rmm,
        'maxiter': maxiter,
        'xc_thread': False,
        'txt': txt}
if use_cuda:
    args['gpu'] = {'cuda': True, 'hybrid_blas': False}
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

