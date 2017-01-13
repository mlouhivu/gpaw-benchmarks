###
### GPAW benchmark: Silicon Crystal
###

from __future__ import print_function
from ase.lattice import bulk
from gpaw import GPAW, Mixer, ConvergenceError
from gpaw.mpi import size, rank
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

# no. of replicates in each dimension (increase to scale up the system)
x = 4
y = 4
z = 4
# other parameters
h = 0.22
kpts = (1,1,1)
txt = 'output.txt'
maxiter = 6

# output benchmark parameters
if rank == 0:
    print("#"*60)
    print("GPAW benchmark: Silicon Crystal")
    print("  dimensions: x=%d, y=%d, z=%d" % (x, y, z))
    print("  grid spacing: h=%f" % h)
    print("  Brillouin-zone sampling: kpts=" + str(kpts))
    print("  MPI tasks: %d" % size)
    print("  using CUDA: " + str(use_cuda))
    print("  using MICs: " + str(use_mic))
    print("#"*60)
    print("")

# compatibility hack for the eigensolver
rmm = RMM_DIIS()
rmm.niter = 2
# setup parameters
args = {'h': h,
        'nbands': -20,
        'width': 0.2,
        'kpts': kpts,
        'xc': 'PBE',
        'mixer': Mixer(0.1, 5, 100),
        'eigensolver': rmm,
        'maxiter': maxiter,
        'parallel': {'sl_auto': True},
        'txt': txt}
if use_cuda:
    args['cuda'] = True

# setup the system
atoms = bulk('Si', cubic=True)
atoms = atoms.repeat((x, y, z))
calc = GPAW(**args)
atoms.set_calculator(calc)

# execute the run
try:
    atoms.get_potential_energy()
except ConvergenceError:
    pass

