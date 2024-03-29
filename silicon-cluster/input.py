###
### GPAW benchmark: Silicon Cluster
###

from __future__ import print_function
from gpaw.mpi import size, rank
from gpaw import GPAW, Mixer, ConvergenceError
from gpaw.occupations import FermiDirac
from gpaw.utilities import h2gpts
from ase.build import bulk
import numpy

# radius of spherical cluster (increase to scale up the system)
radius = 15
# no. of replicates in each dimension
x = int(2 * radius / 5.43) + 1
y = int(2 * radius / 5.43) + 1
z = int(2 * radius / 5.43) + 1
# other parameters
h = 0.18
txt = 'output.txt'
maxiter = 24
bands_per_atom = 2.15
parallel = {'sl_default': (8,8,64)}
# uncomment to use GPUs
#gpu = {'cuda': True, 'hybrid_blas': False}

# check which GPU backend (if any) is used
if 'gpu' in locals():
    use_cuda = gpu.get('cuda', False)
else:
    use_cuda = False

# build a spherical cluster in vacuum
atoms = bulk('Si', cubic=True)
atoms = atoms.repeat((x, y, z))
atoms.center(vacuum=0.0)
center = numpy.diag(atoms.get_cell()) / 2.0
mask = numpy.array([ numpy.linalg.norm(atom.position - center) < radius
    for atom in atoms ])
atoms = atoms[mask]
atoms.rotate((0.1,0.2,0.3), 0.1) # break symmetry
atoms.center(vacuum=5.0)

# setup band parallelisation
bands_per_block = int(radius / 10.0 * 2**10)
parallel['band'] = max(1, size // bands_per_block // 2 * 2)
while (size % parallel['band']):
    parallel['band'] += 2

# calculate the number of electronic bands
nbands = int(len(atoms) * bands_per_atom)
nbands -= nbands % 16
while (nbands % parallel['band']):
    nbands += 2

# calculate the number of grid points
gpts = h2gpts(h, atoms.get_cell(), idiv=16)

# output benchmark parameters
if rank == 0:
    print("#"*60)
    print("GPAW benchmark: Silicon Cluster")
    print("  radius: %.1f" % radius)
    print("  grid spacing: %.3f" % h)
    print("  MPI tasks: %d" % size)
    print("  using GPU: " + str(use_cuda))
    print("#"*60)
    print("")

# setup parameters
args = {'gpts': gpts,
        'nbands': nbands,
        'occupations': FermiDirac(0.05),
        'xc': 'LDA',
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

# setup the calculator
calc = GPAW(**args)
atoms.set_calculator(calc)

# execute the run
try:
    atoms.get_potential_energy()
except ConvergenceError:
    pass

