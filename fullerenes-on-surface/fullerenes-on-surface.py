###
### GPAW benchmark: Carbon Fullerenes on a Lead Surface
###

from __future__ import print_function
from ase.io import read
from gpaw import GPAW, Mixer, ConvergenceError
from gpaw.eigensolvers.rmm_diis import RMM_DIIS
from gpaw.mpi import size, rank
from gpaw import use_mic

# run parameters
h = 0.22
kpt = 2
# other parameters
txt = 'output.txt'
maxiter = 15
conv = {'eigenstates' : 1e-4, 'density' : 1e-2, 'energy' : 1e-3}
input_coords = 'POSCAR'

# output benchmark parameters
if use_mic:
    mic_yesno = 'YES'
else:
    mic_yesno = 'NO'
print("#"*60)
print("GPAW benchmark: Carbon Fullerenes on a Lead Surface")
print("  grid spacing: h=%f" % h)
print("  Brillouin-zone sampling: kpts=(%d,%d,1)" % (kpt, kpt))
print("  MPI task: %d out of %d" % (rank, size))
print("  using MICs: " + mic_yesno)
print("#"*60)
print("")

# setup the system
atoms = read(input_coords)
calc = GPAW(h=h, nbands=-180, width=0.2,
            kpts=(kpt,kpt,1), xc='PBE',
            eigensolver=RMM_DIIS(niter=2),
            mixer=Mixer(0.1, 5, 100),
            parallel={'sl_default': (4,4,64)},
            maxiter=maxiter, txt=txt 
           )
atoms.set_calculator(calc)

# execute the run
try:
    atoms.get_potential_energy()
except ConvergenceError:
    pass

