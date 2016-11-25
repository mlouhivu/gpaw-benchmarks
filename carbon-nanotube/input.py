###
### GPAW benchmark: Carbon Nanotube
###

from __future__ import print_function
try:
    from ase.build import nanotube
except ImportError:
    from ase.structure import nanotube
from gpaw import GPAW, Mixer, PoissonSolver, ConvergenceError
from gpaw.eigensolvers.rmm_diis import RMM_DIIS
from gpaw.mpi import size, rank
try:
    from gpaw import use_mic
except ImportError:
    use_mic = False

# dimensions of the nanotube
n = 6
m = 6
length = 10
# other parameters
txt = 'output.txt'
maxiter = 16
conv = {'eigenstates' : 1e-4, 'density' : 1e-2, 'energy' : 1e-3}

# output benchmark parameters
if rank == 0:
    print("#"*60)
    print("GPAW benchmark: Carbon Nanotube")
    print("  nanotube dimensions: n=%d, m=%d, length=%d" % (n, m, length))
    print("  MPI task: %d out of %d" % (rank, size))
    print("  using MICs: " + str(use_mic))
    print("#"*60)
    print("")

# setup the system
atoms = nanotube(n, m, length)
calc = GPAW(h=0.2, nbands=-60, width=0.1,
            poissonsolver=PoissonSolver(eps=1e-12),
            eigensolver=RMM_DIIS(keep_htpsit=True),
            maxiter=maxiter,
            mixer=Mixer(0.1, 5, 50),
            convergence=conv, txt=txt)
atoms.set_calculator(calc)

# execute the run
try:
    atoms.get_potential_energy()
except ConvergenceError:
    pass

