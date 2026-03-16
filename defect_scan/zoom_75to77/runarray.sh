#!/bin/bash
#SBATCH --exclusive
#SBATCH -a 1-20
#SBATCH -o mpb-calculation.o ## Make one output file for all members of job array since otherwise file management becomes cumbersome
source /etc/profile
#module load mpi/openmpi-4.1.8
export resolution=16
export n=$SLURM_ARRAY_TASK_ID
export m=$SLURM_ARRAY_TASK_COUNT
export supercell=5
./runlattice.sh $n $m $supercell $resolution
