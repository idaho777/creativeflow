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
        '--_output_dir', action='store', type=str, default='',
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

    # Set active camera
    bpy.context.scene.camera = cam

    orig_start = bpy.context.scene.frame_start
    # bpy.context.scene.frame_start = orig_start + args.offset_scene_start_frame_by
    # if args.offset_scene_end_frame_by > 0:
    #     bpy.context.scene.frame_end = orig_start + args.offset_scene_end_frame_by

    # Set frame numbers
    scene = bpy.context.scene
    start_frame = scene.frame_start
    end_frame = scene.frame_end
    print('{}: start_frame - {}: end_frame'.format(start_frame, end_frame))

    # Convert camera convention from blender to opengl
    blend_2_opengl = mathutils.Matrix.Rotation(math.radians(-90), 4, 'X')

    # Setup data for the NeRF format
    train_frames_list = []
    test_frames_list = []
    val_frames_list = []

    random.seed(10)
    for i in range(start_frame, end_frame+1):
        frame_num = i + 1   # Creative flow starts at 1
        scene.frame_set(frame_num)

        camera_world_matrix = cam.matrix_world
        opengl_camera_world_matrix = blend_2_opengl * camera_world_matrix
        transform_matrix = [list(r) for r in opengl_camera_world_matrix]

        img_name = "frame{}".format('%06d' % frame_num)
        img_file_name = "{}.png".format(img_name)
        src_img_path = os.path.join(args.frame_source_dir, img_file_name)

        train_img_path = os.path.join(args.frame_output_dir, args.train_output_prefix, img_file_name)
        train_entry = {}
        train_entry["file_path"] = os.path.join(args.train_output_prefix, img_name)
        train_entry["transform_matrix"] = transform_matrix
        train_frames_list.append(train_entry)
        shutil.copyfile(src_img_path, train_img_path)

        # Put half in test and half in val
        if (i % 2 == 0):
            test_img_path = os.path.join(args.frame_output_dir, args.test_output_prefix, img_file_name)
            test_entry = {}
            test_entry["file_path"] = os.path.join(args.test_output_prefix, img_name)
            test_entry["transform_matrix"] = transform_matrix
            test_frames_list.append(test_entry)
            shutil.copyfile(src_img_path, test_img_path)
        else:
            val_img_path = os.path.join(args.frame_output_dir, args.val_output_prefix, img_file_name)
            val_entry = {}
            val_entry["file_path"] = os.path.join(args.val_output_prefix, img_name)
            val_entry["transform_matrix"] = transform_matrix
            val_frames_list.append(val_entry)
            shutil.copyfile(src_img_path, val_img_path)

    # Create json dict
    transform_dict = {}
    transform_dict["camera_angle_x"] = cam.data.angle_x
    transform_dict["frames"] = train_frames_list
    # Create json transform_file
    transform_train_json = os.path.join(args.frame_output_dir, "transforms_{}.json".format(args.train_output_prefix))
    with open(transform_train_json, 'w') as f:
        json.dump(transform_dict, f)