#!/bin/bash
#SBATCH --exclusive
#SBATCH -o mpb-calculation.o ## Make one output file for all members of job array since otherwise file management becomes cumbersome
source /etc/profile
module load mpi
./runlattice.sh
