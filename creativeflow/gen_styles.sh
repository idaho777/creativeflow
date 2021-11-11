#!/bin/sh

BLEND=$1
PIPELINE=$2
OUTDIR=$3

./datagen/camera_coordinates_nerf.sh $BLEND $PIPELINE/shape/cam0/composite_frame/style.original $OUTDIR/original
./datagen/camera_coordinates_nerf.sh $BLEND $PIPELINE/shape/cam0/raw_frame/outlines/line0.pen1 $OUTDIR/sketch
