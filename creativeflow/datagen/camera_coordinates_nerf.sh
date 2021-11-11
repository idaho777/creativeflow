#!/bin/bash -e
set -o nounset

# Get the directory where current script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

CDIR=`pwd`

USAGE="$0 <blend_path> <image_source> <output_dir>

Run script to extract the camera coordinates from the animation.  The camera 
coordinates will be stored in the ______ format.

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

mkdir -p $CAM_ODIR
mkdir -p $CAM_ODIR/train
mkdir -p $CAM_ODIR/test
mkdir -p $CAM_ODIR/val

LOGFILE=$LOGDIR/log_camera.txt
blender --background --python-exit-code 1 --factory-startup ${BLENDFILE} \
        --python blender/camera_main_nerf.py --\
        --frame_source_dir=$SDIR\
        --frame_output_dir=$CAM_ODIR \
        --train_output_prefix=train\
        --test_output_prefix=test\
        --val_output_prefix=val\
        > $LOGFILE 2>&1
