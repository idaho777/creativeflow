"""
Extract camera transform matrices from the blender animations as a json file.
"""
import bpy

import argparse
import json
import math
import mathutils
import os
import random
import shutil
import sys


# Add to path to make sure we can import modules while running inside Blender.
__sdir = os.path.dirname(os.path.realpath(__file__))
if __sdir not in sys.path:
    sys.path.append(__sdir)

import geo_util
import io_util

if __name__ == "__main__":
    # Parse Arguments after --
    parser = argparse.ArgumentParser(
        description='Configurable utility to modify blend and/or render images/flow/metadata.')

    parser.add_argument(
        '--fbx_file', action='store', type=str, default='',
        help='If set, will set image output to <frame_output_prefix><frame#>.PNG; ' +
        'should include full path.')
    parser.add_argument(
        '--output_blend', action='store', type=str, default='',
        help='If set, will set image output to <frame_output_prefix><frame#>.PNG; ' +
        'should include full path.')

    argv = sys.argv
    if "--" not in argv:
        argv = []  # as if no args are passed
    else:
        argv = argv[argv.index("--") + 1:]
    args = parser.parse_args(argv)

    # Get single camera
    cam = geo_util.get_single_camera_or_die()
    camera_angle_x = cam.data.angle_x

    # Set active camera
    bpy.context.scene.camera = cam

    orig_start = bpy.context.scene.frame_start

    # Get camera attributes
    view_dim = 2 * ((cam.data.sensor_width/2) / cam.data.lens) * 4
    view_bounds = 0.8*view_dim

    # Import fbx file
    # This is to get scale factor.  transform_apply moves the model away from the origin for some reason.
    # Current solution is to import, get scale_factor of model to fit in camera view, delete model, and
    # re-import the character with global_scale=scale_factor.
    bpy.ops.import_scene.fbx(
        filepath=args.fbx_file,
        axis_forward='-Y',
        axis_up='Z')

    model = bpy.data.objects['Armature']

    # Get camera attributes

    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    # Scale+translate model to fit within view box
    model.location.z = 0
    min_bbox_dim = min(model.dimensions.x, model.dimensions.y)
    scale_factor = view_bounds/min_bbox_dim
    model.scale = scale_factor * model.scale

    # Save new blend file
    file_name = os.path.basename(args.fbx_file)
    file_name = os.path.splitext(file_name)[0]

    bpy.ops.wm.save_as_mainfile(filepath=args.output_blend)
    print(args.output_blend)
