###
### GPAW benchmark: Tin Foil
###

from __future__ import print_function
from gpaw.mpi import size, rank
from gpaw import GPAW, Mixer, ConvergenceError
from gpaw.occupations import FermiDirac
from ase.lattice.tetragonal import CenteredTetragonal

# no. of replicates in each dimension (increase to scale up the system)
x = 3
y = 4
z = 2
# other parameters
h = 0.22
kpts = (2,2,1)
txt = 'output.txt'
maxiter = 6
parallel = {'sl_auto': True}
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
    print("GPAW benchmark: Tin Foil")
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
    args['gpu'] = gpu
    args['xc_thread'] = False
try:
    args['parallel'] = parallel
except: pass

# setup the system
atoms = CenteredTetragonal(directions=[[1,-1,0], [1,1,-2], [1,1,1]],
        size=(x,y,z), symbol='Sn', pbc=(1,1,0))
atoms.center(vacuum=6.0, axis=2)
calc = GPAW(**args)
atoms.set_calculator(calc)

# execute the run
try:
    atoms.get_potential_energy()
except ConvergenceError:
    pass

