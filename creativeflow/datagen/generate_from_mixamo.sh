#!/bin/bash -e
set -o nounset

# Get the directory where current script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

CDIR=`pwd`

USAGE="$0 <blend_path> <mixamo_fbx_path> <output_path>

Run script to generate turnaround images of fbx assets.

If you a reading this, this is currently being tested.
"

if [ "$#" -ne "3" ]; then
    echo "ERROR: 3 arguments expected; $# found"
    echo "$USAGE"
    exit 1
fi

BLENDFILE=$1
SDIR=$2
ODIR=$3
LOGDIR=.

# Ensure we can deal with files with spaces
OIFS="$IFS"
IFS=$'
'

CAM_ODIR=$ODIR/
LOGFILE=$LOGDIR/log_camera.txt

export ABCV_COLORS=colors.txt

i=0
for f in ${SDIR}*.fbx; do
    FILENAME=$(basename -- $f)
    FILENAME=${FILENAME%.*}

    CURRODIR="${ODIR}${FILENAME}/"
    CURROBLEND="${CURRODIR}${FILENAME}.blend"
    mkdir -p $CURRODIR
    
    # Create directory for $FILE
    # Create blender file with fbx loaded
    blender --background --python-exit-code 1 --factory-startup ${BLENDFILE} \
            --python blender/load_mixamo_fbx.py --\
            --fbx_file=$f\
            --output_blend=$CURROBLEND
            > $LOGFILE 2>&1

    # call pipeline with file name 
    ./datagen/pipeline.sh -n 1 -s:0:1:2:3:4:5:7:8:9:10:11:\
            -L pen1\
            -m flat\
            $CURROBLEND\
            $CURRODIR "--width=800 --height=800"
done

# blender --background --python-exit-code 1 --factory-startup ${BLENDFILE} \
#         --python blender/camera_main_nerf.py --\
#         --frame_source_dir=$SDIR\
#         --frame_output_dir=$CAM_ODIR \
#         --train_output_prefix=train\
#         --test_output_prefix=test\
#         --val_output_prefix=val\
#         > $LOGFILE 2>&1
