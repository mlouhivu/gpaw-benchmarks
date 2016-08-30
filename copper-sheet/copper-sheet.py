###
### GPAW benchmark: Copper Sheet
###

from __future__ import print_function
from ase.lattice.cubic import FaceCenteredCubic
from ase.lattice.surface import add_vacuum
from gpaw import GPAW, Mixer, ConvergenceError
from gpaw.eigensolvers.rmm_diis import RMM_DIIS
from gpaw.mpi import size, rank
try:
    from gpaw import use_mic
except ImportError:
    use_mic = False

# no. of replicates in each dimension (increase to scale up the system)
x = 4
y = 2
z = 3
# other parameters
h = 0.22
kpts = (8,4,1)
txt = 'output.txt'
maxiter = 6
conv = {'eigenstates' : 1e-4, 'density' : 1e-2, 'energy' : 1e-3}

# output benchmark parameters
if rank == 0:
    print("#"*60)
    print("GPAW benchmark: Copper Sheet")
    print("  dimensions: x=%d, y=%d, z=%d" % (x, y, z))
    print("  grid spacing: h=%f" % h)
    print("  Brillouin-zone sampling: kpts=" + str(kpts))
    print("  MPI task: %d out of %d" % (rank, size))
    print("  using MICs: " + str(use_mic))
    print("#"*60)
    print("")

# setup the system
atoms = FaceCenteredCubic(directions=[[1,-1,0], [1,1,-2], [1,1,1]],
        size=(x,y,z), symbol='Cu', pbc=(1,1,0))
#add_vacuum(atoms, 10.0)
atoms.center(vacuum=6.0, axis=2)
calc = GPAW(h=h, nbands=-20, width=0.2,
            kpts=kpts, xc='PBE',
            maxiter=maxiter,
            txt=txt, eigensolver=RMM_DIIS(niter=2),
            parallel={'sl_auto': True},
            mixer=Mixer(0.1, 5, 100),
           )
atoms.set_calculator(calc)

# execute the run
try:
    atoms.get_potential_energy()
except ConvergenceError:
    pass

