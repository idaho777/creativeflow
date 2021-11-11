#!/bin/bash -e
set -o nounset

# Get the directory where current script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

CDIR=`pwd`

USAGE="$0 <blend_path> <output_dir>

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
ODIR=$2
LOGDIR=.

# Ensure we can deal with files with spaces
OIFS="$IFS"
IFS=$'
'

mkdir -p $CAM_ODIR

LOGFILE=$LOGDIR/log_camera.txt
blender --background --python-exit-code 1 --factory-startup ${BLENDFILE} \
        --python blender/camera_main.py --\
        --output_dir=$ODIR \
        > $LOGFILE 2>&1
