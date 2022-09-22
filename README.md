## Description

Set of benchmarks for GPAW (https://gitlab.com/gpaw/gpaw), a density-functional
theory (DFT) program for ab initio electronic structure calculations.

## Usage

Copy input files to your work directory and run GPAW on the `input.py` script,
e.g.
```
git clone https://github.com/mlouhivu/gpaw-benchmarks
cp -r gpaw-benchmarks/carbon-nanotube $WRKDIR/
cd $WRKDIR/carbon-nanotube
mpirun -np 256 gpaw-python input.py
```

The size of a benchmark system may optionally be scaled (to some extend) by
modifying the run parameters in the GPAW input script (`input.py`).
