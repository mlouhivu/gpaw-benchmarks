###
### GPAW benchmark: Carbon Nanotube
###

from __future__ import print_function
try:
    from ase.build import nanotube
except ImportError:
    from ase.structure import nanotube
from gpaw import GPAW, Mixer, PoissonSolver, ConvergenceError
from gpaw.occupations import FermiDirac
from gpaw.mpi import size, rank
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

# dimensions of the nanotube
n = 6
m = 6
length = 10
# other parameters
txt = 'output.txt'
maxiter = 16
conv = {'eigenstates' : 1e-4, 'density' : 1e-2, 'energy' : 1e-3}
# uncomment to use ScaLAPACK
#parallel = {'sl_auto': True}

# output benchmark parameters
if rank == 0:
    print("#"*60)
    print("GPAW benchmark: Carbon Nanotube")
    print("  nanotube dimensions: n=%d, m=%d, length=%d" % (n, m, length))
    print("  MPI tasks: %d" % size)
    print("  using CUDA (GPGPU): " + str(use_cuda))
    print("  using pyMIC (KNC) : " + str(use_mic))
    print("  using CPU (or KNL): " + str(use_cpu))
    print("#"*60)
    print("")

# setup parameters
args = {'h': 0.2,
        'nbands': -60,
        'occupations': FermiDirac(0.1),
        'mixer': Mixer(0.1, 5, 50),
        'poissonsolver': PoissonSolver(eps=1e-12),
        'eigensolver': 'rmm-diis',
        'maxiter': maxiter,
        'convergence': conv,
        'txt': txt}
if use_cuda:
    args['cuda'] = True
try:
    args['parallel'] = parallel
except: pass

# setup the system
atoms = nanotube(n, m, length)
atoms.center(vacuum=4.068, axis=0)
atoms.center(vacuum=4.068, axis=1)
calc = GPAW(**args)
atoms.set_calculator(calc)

# execute the run
try:
    atoms.get_potential_energy()
except ConvergenceError:
    pass

