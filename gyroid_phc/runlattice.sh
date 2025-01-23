#!/bin/bash
export OPENBLAS_NUM_THREADS=1
IFS=$'\n';
mpirun mpb-mpi lattice.ctl 2>&1 | tee dispersion.log
unset IFS;
