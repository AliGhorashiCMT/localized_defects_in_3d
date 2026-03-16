#!/bin/bash
export OPENBLAS_NUM_THREADS=1
IFS=$'\n';
mpb epsin=11 r1=0.18 r2=0.18 lattice.ctl 2>&1 | tee dispersion.log
unset IFS;
