#!/bin/bash
export OPENBLAS_NUM_THREADS=1
IFS=$'\n';
mpb $(cat symmetry_ops.sh) lattice-symeigs.ctl | tee unitcell-symeigs.log
unset IFS;
