###
### GPAW benchmark: Silicon Crystal
###

from __future__ import print_function
from ase.lattice import bulk
from gpaw import GPAW, Mixer, ConvergenceError
from gpaw.eigensolvers.rmm_diis import RMM_DIIS
from gpaw.mpi import size, rank
from gpaw import use_mic

# no. of replicates in each dimension (increase to scale up the system)
x = 2
y = 1
z = 1
# other parameters
h = 0.22
kpt = 1
txt = 'output.txt'
maxiter = 15
conv = {'eigenstates' : 1e-4, 'density' : 1e-2, 'energy' : 1e-3}

# output benchmark parameters
if use_mic:
    mic_yesno = 'YES'
else:
    mic_yesno = 'NO'
print("#"*60)
print("GPAW benchmark: Silicon Crystal")
print("  dimensions: x=%d, y=%d, z=%d" % (x, y, z))
print("  grid spacing: h=%f" % h)
print("  Brillouin-zone sampling: kpts=(%d,%d,%d)" % (kpt, kpt, kpt))
print("  MPI task: %d out of %d" % (rank, size))
print("  using MICs: " + mic_yesno)
print("#"*60)
print("")

# setup the system
atoms = bulk('Si', cubic=True)
atoms = atoms.repeat((x, y, z))
calc = GPAW(h=h, nbands=-20, width=0.2,
            kpts=(kpt,kpt,kpt), xc='PBE',
            maxiter=maxiter,
            txt=txt, eigensolver=RMM_DIIS(niter=2),
            mixer=Mixer(0.1, 5, 100),
           )
atoms.set_calculator(calc)

# execute the run
try:
    atoms.get_potential_energy()
except ConvergenceError:
    pass

