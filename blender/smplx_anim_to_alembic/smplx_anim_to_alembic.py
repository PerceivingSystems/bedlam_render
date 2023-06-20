# SPDX-License-Identifier: GPL-2.0-or-later
# Copyright (c) 2023 Max Planck Society
#
# Convert SMPL-X animation in .npz format to Alembic .abc geometry cache
#
# Notes:
# + Running via command-line: blender --background --python smplx_anim_to_alembic.py -- --input /path/to/npz --output /path/to/abc
#

import argparse
import bpy
from pathlib import Path
import sys
import time

##################################################
# Globals
##################################################
smplx_animation_path = Path("smplx_animation.npz")
output_path = Path("smplx_animation.abc")

def convert_to_abc(smplx_animation_path, output_path):
    if (not smplx_animation_path.exists()) or (smplx_animation_path.suffix != ".npz"):
        print(f"ERROR: Invalid input path: {smplx_animation_path}")
        return False

    if output_path.suffix != ".abc":
        print(f"ERROR: Invalid output path: {output_path}")
        return False

    # Import animation
    bpy.ops.object.smplx_add_animation(filepath=str(smplx_animation_path), anim_format="SMPL-X", keyframe_corrective_pose_weights=True, target_framerate=30)

    # Export Alembic
    output_path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.object.smplx_export_alembic(filepath=str(output_path))
    return True    

##############################################################################
# Main
##############################################################################
if __name__== "__main__":
    # Parse command-line arguments when invoked via `blender --background smplx_anim_to_alembic.py -- --input in.npz --output out.abc`
    if bpy.app.background:
        if "--" in sys.argv:
            argv = sys.argv[sys.argv.index("--") + 1:]  # get all args after "--"

            parser = argparse.ArgumentParser(description="Convert SMPL-X animation in .npz format to Alembic .abc geometry cache")

            parser.add_argument("--input", required=True, type=str, help="Path to .npz input file")
            parser.add_argument("--output", required=True, type=str, help="Path to .abc output file")
            args = parser.parse_args(argv)
            smplx_animation_path = Path(args.input)
            output_path = Path(args.output)

    print(f"Converting: {smplx_animation_path} => {output_path}")
    start_time = time.perf_counter()
    convert_to_abc(smplx_animation_path, output_path)
    print(f"  Finished. Time: {(time.perf_counter() - start_time):.1f}s")