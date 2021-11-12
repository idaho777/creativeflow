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


    # Import fbx file
    bpy.ops.import_scene.fbx(
        filepath=args.fbx_file,
        axis_forward='-Y',
        axis_up='Z')

    model = bpy.data.objects['Armature']
    bpy.data.armatures['Armature'].layers[1] = True     # Hide skeleton
    bpy.data.armatures['Armature'].layers[0] = False

    # Get camera attributes
    view_dim = 2 * ((cam.data.sensor_width/2) / cam.data.lens) * cam.location.length
    view_bounds = 0.8*view_dim

    print(model.location)
    print(model.scale)
    print(model.dimensions)
    # Scale+translate model to fit within view box
    max_bbox_dim = max(model.dimensions.x, model.dimensions.y)
    scale_factor = view_bounds / max_bbox_dim
    model.scale = scale_factor * model.scale
    model.location.z = model.location.z - (scale_factor*model.dimensions.y/2)
    # model.location.z = model.location.z - (model.dimensions.y/2)

    # model.select = True

    # bpy.ops.object.transform_apply(location=True, scale=True)

    print(model.location)
    print(model.scale)
    print(model.dimensions)
    # Save new blend file
    file_name = os.path.basename(args.fbx_file)
    file_name = os.path.splitext(file_name)[0]

    bpy.ops.wm.save_as_mainfile(filepath=args.output_blend)
    print(args.output_blend)
