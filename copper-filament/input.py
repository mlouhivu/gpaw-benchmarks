###
### GPAW benchmark: Copper Filament
###

from __future__ import print_function
from gpaw.mpi import size, rank
from gpaw import GPAW, Mixer, ConvergenceError
from gpaw.occupations import FermiDirac
from ase.lattice.cubic import FaceCenteredCubic
try:
    from gpaw.eigensolvers.rmm_diis import RMM_DIIS
except ImportError:
    from gpaw.eigensolvers.rmmdiis import RMMDIIS as RMM_DIIS
try:
    from gpaw import use_cuda
    use_cuda = True
except ImportError:
    use_cuda = False

# no. of replicates in each dimension (increase to scale up the system)
x = 3
y = 2
z = 4
# other parameters
h = 0.22
kpts = (1,1,8)
txt = 'output.txt'
maxiter = 24
parallel = {'sl_default': (2,2,64)}

# output benchmark parameters
if rank == 0:
    print("#"*60)
    print("GPAW benchmark: Copper Filament")
    print("  dimensions: x=%d, y=%d, z=%d" % (x, y, z))
    print("  grid spacing: h=%f" % h)
    print("  Brillouin-zone sampling: kpts=" + str(kpts))
    print("  MPI tasks: %d" % size)
    print("  using GPU: " + str(use_cuda))
    print("#"*60)
    print("")

# setup parameters
args = {'h': h,
        'nbands': -20,
        'occupations': FermiDirac(0.2),
        'kpts': kpts,
        'xc': 'PBE',
        'mixer': Mixer(0.1, 5, 100),
        'eigensolver': 'rmm-diis',
        'maxiter': maxiter,
        'txt': txt}
if use_cuda:
    args['gpu'] = {'cuda': True, 'hybrid_blas': False}
    args['xc_thread'] = False
try:
    args['parallel'] = parallel
except: pass

# setup the system
atoms = FaceCenteredCubic(directions=[[1,-1,0], [1,1,-2], [1,1,1]],
        size=(x,y,z), symbol='Cu', pbc=(0,0,1))
atoms.center(vacuum=6.0, axis=0)
atoms.center(vacuum=6.0, axis=1)
calc = GPAW(**args)
atoms.set_calculator(calc)

# execute the run
try:
    atoms.get_potential_energy()
except ConvergenceError:
    pass

