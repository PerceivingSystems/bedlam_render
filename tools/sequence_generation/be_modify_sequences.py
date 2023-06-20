#!/usr/bin/env python3
# Copyright (c) 2023 Max Planck Society
# License: https://bedlam.is.tuebingen.mpg.de/license.html
#
# Modify crowd sequence
#

import csv
import json
from math import sin, cos, radians
from pathlib import Path
import random
import re
import sys
from typing import NamedTuple

# Globals
SUBJECT_GENDER_PATH = Path("../../config/gender.csv")                       # Gender information for each subject
TEXTURES_OVERLAY_PATH = Path("../../config/textures_clothing_overlay.json") # List of available overlay textures per gender
WHITELIST_HAIR_PATH = Path("../../config/whitelist_hair.json")

# Predefined configurations
# Notes:
#   hfov = 65.470451 : 28mm lens on 36x20.25 DSLR filmback
class ConfigCamera(NamedTuple):
    hfov: float = -1.0 # Default: use existing hfov from source
    x_offset_max: float = 0.0
    y_offset_max: float = 0.0
    z_offset_max: float = 0.0
    yaw_min: float = 0.0
    yaw_max: float = 0.0
    pitch_min: float = 0.0
    pitch_max: float = 0.0
    roll_min: float = 0.0
    roll_max: float = 0.0
    hfov: float = 0.0
    override_cam_position: bool = False
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    pitch_from_height: bool = False
    z_min: float = 100.0
    pitch_z_min: float = 5.0
    z_max: float = 250.0
    pitch_z_max: float = -40.0

configs_camera = {}

# Default camera configuration
config_default = ConfigCamera()
configs_camera["cam_default"] = config_default

configs_camera["cam_random_a"] = ConfigCamera(x_offset_max=100.0, y_offset_max=100.0, z_offset_max=15.0, yaw_min=-5, yaw_max=5, pitch_min=-15, pitch_max=5, roll_min=-3, roll_max=3)

configs_camera["cam_random_b"] = ConfigCamera(x_offset_max=0.0, y_offset_max=0.0, z_offset_max=0.0, yaw_min=0, yaw_max=0, pitch_min=-18, pitch_max=3, roll_min=-3, roll_max=3)

configs_camera["cam_random_c"] = ConfigCamera(x_offset_max=10.0, y_offset_max=10.0, z_offset_max=5.0, yaw_min=-3, yaw_max=3, pitch_min=-18, pitch_max=3, roll_min=-3, roll_max=3)

configs_camera["cam_random_d"] = ConfigCamera(x_offset_max=10.0, y_offset_max=10.0, z_offset_max=5.0, yaw_min=-3, yaw_max=3, pitch_min=-5, pitch_max=3, roll_min=-3, roll_max=3)

configs_camera["cam_random_e"] = ConfigCamera(x_offset_max=10.0, y_offset_max=10.0, z_offset_max=5.0, yaw_min=-3, yaw_max=3, pitch_min=-10, pitch_max=3, roll_min=-3, roll_max=3)

configs_camera["cam_random_f"] = ConfigCamera(override_cam_position=True, x = -1000, z = 170, x_offset_max=10.0, y_offset_max=10.0, z_offset_max=5.0, yaw_min=-3, yaw_max=3, pitch_min=-10, pitch_max=3, roll_min=-3, roll_max=3)

configs_camera["cam_random_g"] = ConfigCamera(hfov=25, override_cam_position=True, x = -1000, z = 170, x_offset_max=10.0, y_offset_max=10.0, z_offset_max=5.0, yaw_min=-1, yaw_max=1, pitch_min=-5, pitch_max=2, roll_min=-3, roll_max=3)

configs_camera["cam_random_h"] = ConfigCamera(x_offset_max=10.0, y_offset_max=10.0, z_offset_max=5.0, yaw_min=-3, yaw_max=3, pitch_min=-18, pitch_max=-10, roll_min=-3, roll_max=3)

configs_camera["cam_random_i"] = ConfigCamera(x_offset_max=10.0, y_offset_max=10.0, z_offset_max=5.0, yaw_min=-3, yaw_max=3, pitch_min=0, pitch_max=3, roll_min=-3, roll_max=3)


# Low camera, world ground plane height at 263.75
configs_camera["cam_stadium_a"] = ConfigCamera(override_cam_position=True, x = -1000, z = (263.75 + 15.0), x_offset_max=10.0, y_offset_max=10.0, z_offset_max=5.0, yaw_min=-3, yaw_max=3, pitch_min=5, pitch_max=15, roll_min=-3, roll_max=3)

# High camera, world ground plane height at 263.75
configs_camera["cam_stadium_b"] = ConfigCamera(override_cam_position=True, x = -1000, z = (263.75 + 300.0), x_offset_max=10.0, y_offset_max=10.0, z_offset_max=5.0, yaw_min=-3, yaw_max=3, pitch_min=-20, pitch_max=-10, roll_min=-3, roll_max=3)
configs_camera["cam_stadium_c"] = ConfigCamera(hfov=65.470451, override_cam_position=True, x = -1000, z = (263.75 + 300.0), x_offset_max=10.0, y_offset_max=10.0, z_offset_max=5.0, yaw_min=-3, yaw_max=3, pitch_min=-25, pitch_max=-5, roll_min=-3, roll_max=3)

configs_camera["cam_stadium_d"] = ConfigCamera(override_cam_position=True, x = -1000, z = (263.75 + 170.0), x_offset_max=10.0, y_offset_max=10.0, z_offset_max=5.0, yaw_min=-3, yaw_max=3, pitch_min=-10, pitch_max=3, roll_min=-3, roll_max=3)

# Closeup camera, 2m distance, 28mm, portrait mode
configs_camera["cam_closeup_a"] = ConfigCamera(hfov=65.470451, override_cam_position=True, x = -200, x_offset_max=10.0, y_offset_max=10.0, z_offset_max=5.0, yaw_min=-2, yaw_max=2, pitch_min=-2, pitch_max=2, roll_min=87, roll_max=93, pitch_from_height=True)
configs_camera["cam_closeup_b"] = ConfigCamera(hfov=39.597752, override_cam_position=True, x = -200, x_offset_max=10.0, y_offset_max=10.0, z_offset_max=5.0, yaw_min=-2, yaw_max=2, pitch_min=-2, pitch_max=2, roll_min=-3, roll_max=3, pitch_from_height=True, pitch_z_min=5, pitch_z_max=-25)

# Zoom camera
configs_camera["cam_zoom_a"] = ConfigCamera(override_cam_position=True, x=-1000.0, z=170.0, x_offset_max=10.0, y_offset_max=10.0, z_offset_max=5.0, yaw_min=-3, yaw_max=3, pitch_min=-10, pitch_max=0, roll_min=-3, roll_max=3)

# Orbit camera
configs_camera["cam_orbit_a"] = ConfigCamera(override_cam_position=True, x=-450.0, z=170.0, x_offset_max=10.0, y_offset_max=10.0, z_offset_max=5.0, yaw_min=-3, yaw_max=3, pitch_min=-15, pitch_max=-5, roll_min=-3, roll_max=3)
configs_camera["cam_orbit_b"] = ConfigCamera(override_cam_position=True, x=-450.0, z=100.0, x_offset_max=10.0, y_offset_max=10.0, z_offset_max=5.0, yaw_min=-3, yaw_max=3, pitch_min=-10, pitch_max=10, roll_min=-3, roll_max=3)

# Big office
configs_camera["cam_bigoffice_a"] = ConfigCamera(override_cam_position=True, x=-350.0, z=170.0, x_offset_max=10.0, y_offset_max=10.0, z_offset_max=5.0, yaw_min=-3, yaw_max=3, pitch_min=-15, pitch_max=-5, roll_min=-3, roll_max=3)

################################################################################

def change_camera(csv_path, config_camera, config_type):

    c = config_camera

    with open(csv_path, "r") as f:
        bodies = f.readlines()

    output = []

    for line in bodies:
        line = line.rstrip()
        if line.startswith("Index"):
            output.append(line + "\n")
            continue
        else:
            items = line.split(",")
            index = int(items[0])
            rowtype = items[1]
            if index == 0:
                line = f"{line};cam_x_offset={c.x_offset_max};cam_y_offset={c.y_offset_max};cam_z_offset={c.z_offset_max};cam_yaw_min={c.yaw_min};cam_yaw_max={c.yaw_max};cam_pitch_min={c.pitch_min};cam_pitch_max={c.pitch_max};cam_roll_min={c.roll_min};cam_roll_max={c.roll_max};cam_config={config_type}"
                output.append(line + "\n")
                continue

            if rowtype == "Group":
                name = items[2]
                if c.override_cam_position:
                    x_start = c.x
                    y_start = c.y
                    if c.pitch_from_height:
                        z_start = random.uniform(c.z_min, c.z_max)
                    else:
                        z_start = c.z
                else:
                    x_start = float(items[3])
                    y_start = float(items[4])
                    z_start = float(items[5])

                x = x_start + random.uniform(-c.x_offset_max, c.x_offset_max)
                y = y_start + random.uniform(-c.y_offset_max, c.y_offset_max)
                z = z_start + random.uniform(-c.z_offset_max, c.z_offset_max)
                yaw = random.uniform(c.yaw_min, c.yaw_max)

                pitch_start = 0.0
                if c.pitch_from_height:
                    t = (z - c.z_min)/(c.z_max - c.z_min) # [0,1]
                    pitch_start = (1 - t) * c.pitch_z_min + t * c.pitch_z_max

                pitch = pitch_start + random.uniform(c.pitch_min, c.pitch_max)
                roll = random.uniform(c.roll_min, c.roll_max)
                comment = items[9]
                if c.hfov > 0:
                    # Use new horizontal field-of-view from configuration
                    match = re.search(r"(.+)camera_hfov=([^;]+)(.*)", comment)
                    if not match:
                        print("ERROR: Cannot find camera_hfov entry in source data")
                        sys.exit(1)

                    comment = match.group(1) + f"camera_hfov={c.hfov}" + match.group(3)

                line = f"{index},{rowtype},{name},{x},{y},{z},{yaw},{pitch},{roll},{comment}"

            output.append(line + "\n")

    csv_output_path = csv_path.parent / csv_path.name.replace(".csv", "_camrandom.csv")
    print(f"Saving modified sequence: {csv_output_path}")
    with open(csv_output_path, "w") as f:
        f.writelines(output)

    return

def change_camera_root(csv_path):

    with open(csv_path, "r") as f:
        bodies = f.readlines()

    output = []

    for line in bodies:
        line = line.rstrip()
        if line.startswith("Index"):
            output.append(line + "\n")
            continue

        items = line.split(",")
        index = int(items[0])
        rowtype = items[1]
        if index == 0:
            line = f"{line};cameraroot_yaw_min=0;cameraroot_yaw_max=360]"
            output.append(line + "\n")
            continue

        if rowtype == "Group":
            cam_root_yaw = random.uniform(0, 360)
            line = f"{line};cameraroot_yaw={cam_root_yaw}"

        output.append(line + "\n")

    csv_output_path = csv_path.parent / csv_path.name.replace(".csv", "_camroot.csv")
    print(f"Saving modified sequence: {csv_output_path}")
    with open(csv_output_path, "w") as f:
        f.writelines(output)

    return

# Rotate camera and bodies in world space (HDRI background and body lighting variation)
def change_sequence_root(csv_path):

    with open(csv_path, "r") as f:
        bodies = f.readlines()

    output = []

    angle = 0.0
    for line in bodies:
        line = line.rstrip()
        if line.startswith("Index"):
            output.append(line + "\n")
            continue
        else:
            items = line.split(",")

            index = int(items[0])
            rowtype = items[1]
            name = items[2]
            x = float(items[3])
            y = float(items[4])
            z = float(items[5])
            yaw  = float(items[6])
            pitch = float(items[7])
            roll = float(items[8])
            comment = items[9]


            if rowtype == "Group":
                angle = random.uniform(0.0, 360.0)

                # Note: we do not need to rotate camera location since it's at origin for HDRI scenes

                yaw_r = yaw + angle
                if yaw_r >= 360.0:
                    yaw_r -= 360.0

                comment += f";angle={angle}"

                line = f"{index},{rowtype},{name},{x},{y},{z},{yaw_r},{pitch},{roll},{comment}"

            elif rowtype == "Body":
                # Rotate body in world space
                sin_a = sin(radians(angle))
                cos_a = cos(radians(angle))

                x_r = cos_a * x - sin_a * y
                y_r = sin_a * x + cos_a * y

                yaw_r = yaw + angle
                if yaw_r >= 360.0:
                    yaw_r -= 360.0

                line = f"{index},{rowtype},{name},{x_r},{y_r},{z},{yaw_r},{pitch},{roll},{comment}"

            output.append(line + "\n")

    csv_output_path = csv_path.parent / csv_path.name.replace(".csv", "_sequenceroot.csv")
    print(f"Saving modified sequence: {csv_output_path}")
    with open(csv_output_path, "w") as f:
        f.writelines(output)

    return

# Replace textured geometry clothing with clothing overlay
def clothing_overlay_replace(csv_path):

    with open(csv_path, "r") as f:
        bodies = f.readlines()

    output = []

    for line in bodies:
        line = line.rstrip()


        if line.startswith("Index"):
            output.append(line + "\n")
            continue

        items = line.split(",")
        index = int(items[0])
        rowtype = items[1]
        subject_animation_index = items[2].split("_")[-1]
        subject = items[2].replace(f"_{subject_animation_index}", "")
        if rowtype == "Body":
            match = re.search(r"(.+)texture_clothing=([^\;]+)(.*)", line)
            if match:
                texture_clothing_overlay = f"{subject}_{match.group(2)}"
                line = match.group(1) + f"texture_clothing_overlay={texture_clothing_overlay}" + match.group(3)

        output.append(line + "\n")

    csv_output_path = csv_path.parent / csv_path.name.replace(".csv", "_overlay.csv")
    print(f"Saving modified sequence: {csv_output_path}")
    with open(csv_output_path, "w") as f:
        f.writelines(output)

    return

# Add textured geometry clothing to files which do not have geometry clothing information
def clothing_overlay_add(csv_path):

    subject_gender = {}
    with open(SUBJECT_GENDER_PATH) as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            subject_gender[row["Name"]] = row["Gender"]

    textures_overlay = {}
    with open(TEXTURES_OVERLAY_PATH) as f:
        textures_overlay = json.load(f)

    current_textures_overlay = { "f": [], "m": [] }

    with open(csv_path, "r") as f:
        bodies = f.readlines()

    output = []

    for line in bodies:
        line = line.rstrip()


        if line.startswith("Index"):
            output.append(line + "\n")
            continue

        items = line.split(",")
        index = int(items[0])
        rowtype = items[1]
        body = items[2]

        if rowtype == "Body":
            match = re.search(r"(.+)_\d\d\d\d", body)
            if not match:
                print("ERROR: Invalid subject name: {body}")
                sys.exit(1)
            subject = match.group(1)

            gender = subject_gender[subject]
            if len(current_textures_overlay[gender]) == 0:
                current_textures_overlay[gender] = list(textures_overlay[gender])

            texture_clothing_overlay = current_textures_overlay[gender].pop(random.randrange(len(current_textures_overlay[gender])))

            line += f";texture_clothing_overlay={texture_clothing_overlay}"

        output.append(line + "\n")

    csv_output_path = csv_path.parent / csv_path.name.replace(".csv", "_overlay.csv")
    print(f"Saving modified sequence: {csv_output_path}")
    with open(csv_output_path, "w") as f:
        f.writelines(output)

    return

# Add hair
def hair_add(csv_path):

    subject_gender = {}
    with open(SUBJECT_GENDER_PATH) as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            subject_gender[row["Name"]] = row["Gender"]

    # Get gender hair whitelelist
    whitelist_hair = {}
    with open(WHITELIST_HAIR_PATH) as f:
        whitelist_hair = json.load(f)

    # Ensure equal use of hair types over all sequences by not using hair from previous sequences if possible.
    current_hair = { 'f':[], 'm':[] }

    with open(csv_path, "r") as f:
        bodies = f.readlines()

    output = []

    for line in bodies:
        line = line.rstrip()


        if line.startswith("Index"):
            output.append(line + "\n")
            continue

        items = line.split(",")
        index = int(items[0])
        rowtype = items[1]
        body = items[2]

        if rowtype == "Body":
            match = re.search(r"(.+)_\d\d\d\d", body)
            if not match:
                print("ERROR: Invalid subject name: {body}")
                sys.exit(1)
            subject = match.group(1)

            gender = subject_gender[subject]

            if len(current_hair[gender]) == 0:
                current_hair[gender] = list(whitelist_hair[gender])

            hair_name = current_hair[gender].pop(random.randrange(len(current_hair[gender])))

            line += f";hair={hair_name}"

        output.append(line + "\n")

    csv_output_path = csv_path.parent / csv_path.name.replace(".csv", "_hair.csv")
    print(f"Saving modified sequence: {csv_output_path}")
    with open(csv_output_path, "w") as f:
        f.writelines(output)

    return

def print_usage():
    print(f"Usage: {sys.argv[0]} INPUTCSVPATH camera CONFIGTYPE", file=sys.stderr)
    print("       %s be_seq.csv camera cam_random_a" % (sys.argv[0]), file=sys.stderr)
    print(configs_camera.keys())
    print(f"Usage: {sys.argv[0]} INPUTCSVPATH cameraroot", file=sys.stderr)
    print(f"Usage: {sys.argv[0]} INPUTCSVPATH sequenceroot", file=sys.stderr)
    print(f"Usage: {sys.argv[0]} INPUTCSVPATH clothing_overlay [add]", file=sys.stderr)
    print(f"Usage: {sys.argv[0]} INPUTCSVPATH hair", file=sys.stderr)
    return

################################################################################
# Main
################################################################################

if len(sys.argv) < 3:
    print_usage()
    sys.exit(1)

csv_path = Path(sys.argv[1])
target_type = sys.argv[2]

if target_type == "camera":
    config_type = sys.argv[3]
    if not config_type in configs_camera:
        print(f"ERROR: Undefined camera type: {config_type}", file=sys.stderr)
        print(configs_camera.keys())
        sys.exit(1)

    change_camera(csv_path, configs_camera[config_type], config_type)
elif target_type == "cameraroot":
    change_camera_root(csv_path)
elif target_type == "sequenceroot":
    change_sequence_root(csv_path)
elif target_type == "clothing_overlay":
    if len(sys.argv) == 4:
        clothing_overlay_add(csv_path)
    else:
        clothing_overlay_replace(csv_path)
elif target_type == "hair":
    hair_add(csv_path)
else:
    print(f"ERROR: Unknown target type: {target_type}", file=sys.stderr)
    sys.exit(1)

sys.exit(0)
