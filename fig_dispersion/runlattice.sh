#!/bin/bash
export OPENBLAS_NUM_THREADS=1
IFS=$'\n';
mpirun mpb-mpi epsin=12.5 r1=0.18 r2=0.18 lattice.ctl 2>&1 | tee dispersion.log
unset IFS;
