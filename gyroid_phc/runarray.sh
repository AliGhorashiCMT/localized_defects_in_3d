#!/bin/bash
#SBATCH --exclusive
#SBATCH -o mpb-calculation.o ## Make one output file for all members of job array since otherwise file management becomes cumbersome
source /etc/profile
module load mpi/openmpi-4.1.5
./runlattice.sh
