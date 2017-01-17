#!/bin/bash
#################################################################
# Wrapper script to launch GPAW jobs with correct affinities    #
#   on Xeon Phi Knights Corner (KNC) MICs                       #
#################################################################

### MACHINE SPECS ###
ndev=2        # number of MIC devices in the system
tpc=4         # number of threads per physical core
nphcores=61   # number of cores per MIC
nphcores=$((nphcores - 1))  # one non-compute core on the MIC
PYMIC_KMP_AFFINITY=compact  # thread affinity on the MIC device
                            # (add ',verbose' to see placement)
### MACHINE SPECS ###

# get some information about the job
ppn=$1
shift
rank=$PMI_RANK
nmpi=$PMI_SIZE

# ranks per device
rpd=$((ppn / ndev))
if [ "$rpd" == "0" ]; then
    rpd=1
fi

# physical cores per device
ncores=$((nphcores / rpd))

# partition number of the current rank on its device
partition=$((rank % rpd))

# offset for the current rank
offset=$((ncores * partition))

# build core selection string
select="${ncores}c,${tpc}t,${offset}o"

# fire up the actual run
log="rank-`printf %03d $rank`.log"
rm -f $log
echo "host `hostname` rank `printf %03d $rank` - $select " |& tee -a $log
export PYMIC_KMP_AFFINITY
export PYMIC_KMP_PLACE_THREADS=$select
env | grep PYMIC |& tee -a $log
$@ |& tee -a $log
