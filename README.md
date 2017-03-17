## Description

Set of benchmarks for GPAW (https://gitlab.com/gpaw/gpaw), a density-functional
theory (DFT) program for ab initio electronic structure calculations.

## Usage

Copy input files to your work directory and run GPAW on the `input.py` script,
e.g.
```
git clone -b prace https://github.com/mlouhivu/gpaw-benchmarks
cp -r gpaw-benchmarks/carbon-nanotube $WRKDIR/
cd $WRKDIR/carbon-nanotube
mpirun -np 256 gpaw-python input.py
```
Example batch job scripts and other potentially useful examples are available
in the `setup/` directory. See e.g. `setup/job-cpu.sh` to get started.

The size of a benchmark system may optionally be scaled (to some extend) by
modifying the run parameters in the GPAW input script (`input.py`).

### Running on accelerators

No special command line options or environment variables are needed to run the
benchmarks on GPGPUs or KNLs (Xeon Phi Knights Landing MICs). One can simply
say e.g.
```
mpirun -np 256 gpaw-python input.py
```

For KNCs (Xeon Phi Knights Corner MICs), one needs to use a wrapper script to
set correct affinities for pyMIC (see `setup/affinity-wrapper.sh` for an
example) and to set two environment variables for GPAW:
```
GPAW_OFFLOAD=1  # to turn on offloading
GPAW_PPN=<no. of MPI tasks per node>
```

For example, in a SLURM system, this could be:
```
GPAW_PPN=12 GPAW_OFFLOAD=1 mpirun -np 256 -bootstrap slurm \
  ./affinity-wrapper.sh gpaw-python input.py
```

Example job scripts (```setup/job-*.sh```) for different accelerator
architectures are provided together with related machine specifications
(```setup/specs.*```) that may offer a helpful starting point (especially for
KNCs).

