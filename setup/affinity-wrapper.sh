#!/bin/bash
#################################################################
# Wrapper script to launch GPAW jobs with correct affinities    #
#   on Xeon Phi Knights Corner (KNC) MICs                       #
#################################################################
# Uses following environment variables:
#   HOST_PE    -- no. of host CPUs
#   HOST_CORES -- no. of CPU cores in a processor
#   MIC_PE     -- no. of MIC cards
#   MIC_CORES  -- no. of MIC cores in a card (N-1 used for compute)
#   MIC_TPC    -- no. of threads per MIC core

# default affinity on the MIC (add ',verbose' to see placement)
[[ ${PYMIC_KMP_AFFINITY:+x} ]] || PYMIC_KMP_AFFINITY=compact

# MPI job size and current rank
nmpi=$PMI_SIZE
rank=$PMI_RANK

# no. of MPI tasks per MIC card
tasks=$(( HOST_PE * HOST_CORES / MIC_PE ))
if [ "$tasks" == "0" ]; then
    tasks=1
fi
# no. of MIC cores per MPI task
cores=$(( (MIC_CORES - 1) / tasks ))
# offset for the current MPI rank
offset=$(( cores * (rank % tasks) ))

# build core selection string
select="${cores}c,${MIC_TPC}t,${offset}o"

# fire up the actual run
log="rank-`printf %03d $rank`.log"
rm -f $log
echo "host `hostname` rank `printf %03d $rank` - $select " |& tee -a $log
export PYMIC_KMP_AFFINITY
export PYMIC_KMP_PLACE_THREADS=$select
env | grep PYMIC |& tee -a $log
$@ |& tee -a $log
