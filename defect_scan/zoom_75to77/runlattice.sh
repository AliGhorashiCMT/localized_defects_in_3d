#!/bin/bash
export n=$1
export m=$2
export resolution=$4
export supercell=$3
export OPENBLAS_NUM_THREADS=1
IFS=$'\n';

defectr=$(echo "round(0.75 + 0.02*(($n-1)/$m), digits=6)" | julia)
echo "n=$n, m=$m, defectr=$defectr, resolution=$resolution, supercell=$supercell"

mpb nbands=300 prefix=\"supercell-${supercell}-${n}-${m}-${resolution}\" defectr=$defectr res=$resolution supercell=$supercell lattice.ctl | tee supercell-$n-$m-$supercell-$resolution.log
unset IFS;
