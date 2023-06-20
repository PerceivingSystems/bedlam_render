#!/usr/bin/env -S python -u
# Copyright (c) 2023 Max Planck Society
# License: https://bedlam.is.tuebingen.mpg.de/license.html
#
# Generate .csv file with desired body positions for multiple animated people per sequence
#
# Dependencies:
# + pip install opencv-python-headless
#
# Notes: Run in unbuffered mode (-u) to immediately see results when piping stdout to tee
#

import copy
import csv
import cv2
from dataclasses import dataclass
import json
from math import radians, tan
import numpy as np
from pathlib import Path
import random
import sys

from be_generate_sequences_crowd_config import *

# Globals
CV_IMAGESIZE = 101 # represents 10m distance with origin in center of image at (50,50)
CV_M_TO_PIXELS = 10
CV_BODY_RADIUS = 5  # 50cm body radius

SMPLX_NPZ_ANIMATION_FOLDER = Path("/mnt/c/bedlam/animations/gendered_ground_truth")

SUBJECT_GENDER_PATH = Path("../../config/gender.csv")               # Gender information for each subject
TEXTURES_BODY_PATH = Path("../../config/textures_body.txt")         # List of available body textures
TEXTURES_CLOTHING_PATH = Path("../../config/textures_clothing.csv") # List of available clothing textures per subject

WHITELIST_PATH = Path("../../config/whitelist_animations.json")     # Per-subject whitelisted animations
#WHITELIST_PATH = Path("../../config/whitelist_animations_highbmihand_20221019.json")

WHITELIST_HAIR_PATH = Path("../../config/whitelist_hair.json")

OUTPUT_IMAGE_ROOT = Path("images")
################################################################################

@dataclass
class SubjectLocationData:
    subject_name: str
    animation_name: str
    frames: int
    bounding_box_area: float
    trans: np.ndarray
    image: np.ndarray
    x: float
    y: float
    yaw: float
    start_frame: int
    used_frames: int


################################################################################
# Helper functions
################################################################################

def get_image_coordinates_from_smplx(imagesize, animation_x, animation_z):
    image_center_x = (imagesize - 1) / 2
    image_center_y = (imagesize - 1) / 2

    # Animation coordinates: X-RightOfBody-FacingAlongPositiveZ, Z-TowardsCamera, [m]
    # OpenCV coordinates: X-Right, Y-Down

    image_x = round(image_center_x + animation_z * CV_M_TO_PIXELS)
    image_y = round(image_center_y - animation_x * CV_M_TO_PIXELS)
    return (image_x, image_y)

def get_image_offset_from_unreal(unreal_x, unreal_y):
    # Unreal coordinates: X-Up, Y-Right, [cm]
    # OpenCV coordinates: X-Right, Y-Down

    image_x = round((unreal_y/100) * CV_M_TO_PIXELS)
    image_y = round((-unreal_x/100) * CV_M_TO_PIXELS)
    return (image_x, image_y)

def transform_image(source_image, unreal_x, unreal_y, unreal_yaw):
    (t_x, t_y) = get_image_offset_from_unreal(unreal_x, unreal_y)

    height, width = source_image.shape
    center = ( (width-1)/2, (height-1)/2 )

    # Rotate source image and then translate it
    # Unreal yaw is left-handed and OpenCV rotations are counter-clockwise
    R = cv2.getRotationMatrix2D(center=center, angle=-unreal_yaw, scale=1)
    source_image_r = cv2.warpAffine(source_image, R, (width, height))

    T = np.float32([[1, 0, t_x], 
                    [0, 1, t_y]])

    source_image_r_t = cv2.warpAffine(source_image_r, T, (width, height))

    return source_image_r_t


def get_location_data(c, grouptype, sequence_index, used_subjects, used_animations, animation_folder):
    location_data = []
    for index, subject in enumerate(used_subjects):
        animation_name = used_animations[index]

        # Load animation data
        filepath = animation_folder / subject / "moving_body_para" / animation_name / "motion_seq.npz"

        with np.load(filepath) as data:
            trans = data["trans"]
            frames = len(trans)

        data = SubjectLocationData(subject, animation_name, frames, 0.0, trans, None, 0, 0, 0, 0, 0)
        location_data.append(data)

    # Find shortest animation sequence length
    maximum_sequence_length = sys.maxsize
    for data in location_data:
        if data.frames < maximum_sequence_length:
            maximum_sequence_length = data.frames

    # Randomize animation start frame
    for data in location_data:
        data.start_frame = random.randint(0, data.frames - maximum_sequence_length)
        data.used_frames = maximum_sequence_length

    # Sort location data by covered bounding box area.
    # Smaller areas are easier to place so we do those at the end.
    location_data_areasorted = []
    for data in location_data:
        trans = data.trans[data.start_frame : (data.start_frame + data.used_frames), :]
        x_min = trans[:,0].min()
        x_max = trans[:,0].max()
        z_min = trans[:,2].min()
        z_max = trans[:,2].max()
        data.bounding_box_area = (x_max - x_min) * (z_max - z_min)

        if len(location_data_areasorted) == 0:
            location_data_areasorted.append(data)
        else:
            for index, list_data in enumerate(location_data_areasorted):
                if data.bounding_box_area > list_data.bounding_box_area:
                    location_data_areasorted.insert(index, data)
                    break

                if index == (len(location_data_areasorted) - 1):
                    location_data_areasorted.append(data)
                    break

    # Generate ground occupancy masks for unmodified animations
    for data in location_data_areasorted:
        radius = CV_BODY_RADIUS
        current_location_image = np.zeros( (CV_IMAGESIZE, CV_IMAGESIZE), dtype=np.uint8)
        trans = data.trans[data.start_frame : (data.start_frame + data.used_frames), :]
        for position in trans:
            # Mark occupied area
            circle_center = get_image_coordinates_from_smplx(CV_IMAGESIZE, position[0], position[2])
            cv2.circle(current_location_image, circle_center, radius, 255, -1)

        # Debug image output
        #cv2.imwrite(f"{data.subject_name}_{data.animation_name}.png", current_location_image)

        # Store image
        data.image = current_location_image

    # Find target locations
    for (index, data) in enumerate(location_data_areasorted):
        print(f"  Processing: {data.subject_name}_{data.animation_name}", file=sys.stderr)

        # Randomize position and yaw and check if leaving area boundary

        # Generate mask to check if animation is leaving the area boundary
        area_boundary_size = (CV_IMAGESIZE - 1) * 2 + 1
        area_boundary_mask = np.ones( (area_boundary_size, area_boundary_size), dtype=np.uint8) * 255

        center_x = round( (area_boundary_size-1) / 2 )
        safety_zone_width_pixels = round( (c.safety_zone_width / 100) * CV_M_TO_PIXELS)
        safety_start_x = center_x - round( safety_zone_width_pixels / 2 )
        safety_end_x = center_x + round( safety_zone_width_pixels / 2 )
        safety_start_y = safety_start_x
        safety_end_y = safety_end_x
        cv2.rectangle(area_boundary_mask, (safety_start_x, safety_start_y), (safety_end_x, safety_end_y), 0, -1)
        #cv2.imwrite(f"area_boundary_mask.png", area_boundary_mask)

        target_image = None
        target_image_location_test_index = 1
        safety_zone_test_index = 1
        x_min = c.x_min
        x_max = c.x_max
        y_min = c.y_min
        y_max = c.y_max

        start_x = round((CV_IMAGESIZE-1)/2)
        start_y = start_x

        while target_image is None:
            if target_image_location_test_index % 5000 == 0:
                offset = 10
                x_min -= offset
                x_max += offset
                y_min -= offset
                y_max += offset
                print(f"  Increasing body area: Location trial={target_image_location_test_index}, x=[{x_min}, {x_max}], y=[{y_min}, {y_max}]", file=sys.stderr)

            # Give up if we cannot find safety zone location within reasonable time
            if safety_zone_test_index % 5000 == 0:
                print(f"  WARNING: Safety zone test failed: Zone trial={safety_zone_test_index}", file=sys.stderr)
                return None

            x = random.uniform(x_min, x_max)
            y = random.uniform(y_min, y_max)
            yaw = random.uniform(c.yaw_min, c.yaw_max)

            ground_trajectory_mask = np.zeros( (area_boundary_size, area_boundary_size), dtype=np.uint8)
            height, width = data.image.shape
            # Copy current template trajectory in larger mask at center
            ground_trajectory_mask[start_y:(start_y + height), start_x:(start_x + width)] = data.image


            ground_trajectory_mask_r_t = transform_image(ground_trajectory_mask, x, y, yaw)

            area_mask_test = cv2.bitwise_and(area_boundary_mask, ground_trajectory_mask_r_t)
            #cv2.imwrite(f"test_r_t_{index}_masked.png", area_mask_test)

            if not np.any(area_mask_test):
                target_image_location_test_index += 1
                # No overlap with outside boundary, we have valid area trajectory and can do occupancy overlap check next
                target_image = transform_image(data.image, x, y, yaw)

                if index > 0:
                    occupancy_test = cv2.bitwise_and(occupancy_image_mask, target_image)
                    if np.any(occupancy_test):
                        # Failed test, we are overlapping, need to try with new location
                        target_image = None
                        continue
                
                # Valid trajectory without occupancy overlap found
                data.x = x
                data.y = y
                data.yaw = yaw
                #cv2.imwrite(f"target_image.png", target_image)
                continue
            else:
                # Safety zone test failed
                safety_zone_test_index += 1

        # Color table (20 entries, generated with distinctipy)
        rgb_colors = [(0.9719224153972289, 0.0006387120046262851, 0.9572435498906621), (0.0, 1.0, 0.0), (0.0, 0.5, 1.0), (1.0, 0.5, 0.0), (0.5, 0.75, 0.5), 
                      (0.30263956385061963, 0.02589151037218751, 0.6757257307743725), (0.8216012497248589, 0.0026428145851382645, 0.20847626796262153), (0.01267507572944171, 0.49697306807148534, 0.17396314179520123), (0.0, 1.0, 1.0), (0.9698728055826683, 0.5021762913810213, 0.7875501077376108), 
                      (1.0, 1.0, 0.0), (0.0, 1.0, 0.5), (0.510314116241271, 0.3232218781514624, 0.09891582182150804), (0.520147512582225, 0.8462498714551937, 0.00708852231806234), (0.5022640147541273, 0.3238721132368306, 0.9748299235270517), 
                      (0.5637646267468693, 0.7935494453374514, 0.9943913298776966), (0.9710018684130394, 0.8195424816067317, 0.46244870837979113), (0.26496132907909453, 0.38952992986967117, 0.5617810079535678), (0.0, 0.0, 1.0), (0.7026382639692401, 0.2676706088672629, 0.4941663340174245)]

        if index == 0:
            occupancy_image_mask = target_image.copy()

            (r, g, b) = rgb_colors[index % len(rgb_colors)]
            occupancy_image = cv2.cvtColor(target_image, cv2.COLOR_GRAY2BGR) * (b, g, r) # bgr
        else:
            occupancy_image_mask = cv2.bitwise_or(occupancy_image_mask, target_image)

            (r, g, b) = rgb_colors[index % len(rgb_colors)]
            occupancy_image = occupancy_image + cv2.cvtColor(target_image, cv2.COLOR_GRAY2BGR) * (b, g, r) # bgr

        #cv2.imwrite(f"occupancy_image.png", occupancy_image)

    # Add camera frustum and save accumulated ground trajectory image
    ground_trajectories = np.zeros( (area_boundary_size, area_boundary_size, 3), dtype=np.uint8)
    ground_trajectories[start_y:(start_y + height), start_x:(start_x + width)] = occupancy_image

    output_root = OUTPUT_IMAGE_ROOT / grouptype / "ground_trajectories"
    output_root.mkdir(parents=True, exist_ok=True)
    output_image_path = output_root / f"ground_trajectories_{sequence_index:06d}.png"
#    cv2.imwrite(str(output_image_path), occupancy_image)
    cv2.imwrite(str(output_image_path), ground_trajectories)

    # Adjust sequence lengths for proper motion blur at beginning and end
    for data in location_data:
        # Due to Unreal (5.0.3) Alembic Python import bug the last frame is invalid and we need to skip it
        data.used_frames -= 1

        # For proper motion blur (temporal sampling) in Unreal we need to have valid data before and after each keyframe.
        # Increment start frame by one so that shortest sequence has a valid previous frame for image frame 0.
        data.start_frame += 1
        data.used_frames -= 1

        # Decrement end frame for proper temporal sampling on last image frame
        data.used_frames -= 1

    return location_data

def get_sequences(c, grouptype, subject_animations, animation_folder):
    num_sequences = c.num_sequences

    sequences = []
    subjects = list(subject_animations.keys())

    if c.unique_sequences:
        input_subjects = list(subjects)
        input_subject_animations = copy.deepcopy(subject_animations)

    sequence_index = 0
    while sequence_index < num_sequences:
        print(f"Generating sequence: {sequence_index}", file=sys.stderr)
        num_subjects = random.randint(c.bodies_min, c.bodies_max)

        if c.unique_sequences:
            if len(subjects) < num_subjects:
                subjects = list(input_subjects)

        current_subjects = list(subjects)

        used_subjects = []
        used_animations = []

        for _ in range(num_subjects):
            # Select target subjects, avoid same subject in same sequence if requested
            # Note: We treat rp_aaron_posed_002 and rp_aaron_posed_009 as different subjects due to different clothing
            current_subject_index = random.randint(0, len(current_subjects)-1)
            current_subject = current_subjects[current_subject_index]
            if c.unique_subjects:
                # Remove selected subject from current_subjects so that it will not be selected on following iterations
                current_subjects.remove(current_subject)

            used_subjects.append(current_subject)

            # Find animation for current subject
            current_animations = subject_animations[current_subject]
            current_animation_index = random.randint(0, len(current_animations)-1)
            current_animation = current_animations[current_animation_index]

            used_animations.append(current_animation)

        # Get sequence bodies location data, sorted by ground area coverage, largest first
        subject_location_data = get_location_data(c, grouptype, sequence_index, used_subjects, used_animations, animation_folder)
        if subject_location_data is not None:
            sequences.append( (f"seq_{sequence_index:06d}", subject_location_data) )
            sequence_index += 1

        if c.unique_sequences:
            # Remove used subjects and animations
            for index, used_subject in enumerate(used_subjects):
                used_animation = used_animations[index]
                subject_animations[used_subject].remove(used_animation)
                if len(subject_animations[used_subject]) == 0:
                    subject_animations[used_subject] = list(input_subject_animations[used_subject])

                subjects.remove(used_subject)

    return sequences


################################################################################
# Main
################################################################################
if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print(f"Usage: {sys.argv[0]} GROUPTYPE [HDRI_PATH]", file=sys.stderr)
        print(configs.keys())
        sys.exit(1)

    grouptype = sys.argv[1]
    if not grouptype in configs:
        print(f"ERROR: Undefined group type: {grouptype}", file=sys.stderr)
        sys.exit(1)
    c = configs[grouptype]

    whitelist_path = WHITELIST_PATH

    hdris_path = None
    if len(sys.argv) > 2:
        hdris_path = sys.argv[2]

    # Get list of whitelisted subject animations
    subject_animations = {}
    with open(whitelist_path) as f:
        subject_animations = json.load(f)

        # Remove subjects which do not have any animations
        subjects = list(subject_animations.keys())
        for subject in subjects:
            if len(subject_animations[subject]) == 0:
                print(f"WARNING: Removing subject without animations: {subject}", file=sys.stderr)
                del(subject_animations[subject])

    subjects = list(subject_animations.keys())

    hdris = None
    hdris_index = 0
    if hdris_path is not None:
        hdris = []
        # Get list of HDRI images
        with open(hdris_path) as f:
            hdris = f.read().splitlines()

    # Get subject gender information
    subject_gender = {}
    with open(SUBJECT_GENDER_PATH) as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            subject_gender[row["Name"]] = row["Gender"]

    # Get list of available body textures
    textures_body_female = []
    textures_body_male = []

    with open(TEXTURES_BODY_PATH) as f:
        lines = f.read().splitlines()
        for line in lines:
            if "_f" in line:
                textures_body_female.append(line)
            else:
                textures_body_male.append(line)

    # Get list of available clothing textures
    textures_clothing = {}
    with open(TEXTURES_CLOTHING_PATH) as f:
        csv_reader = csv.DictReader(f, delimiter=",")
        for row in csv_reader:
            name = row["Name"]
            textures = []
            texture_names = row["Textures"].split(";")
            for texture_name in texture_names:
                textures.append(texture_name)

            textures_clothing[name] = textures

    # Get gender hair whitelelist
    whitelist_hair = {}
    with open(WHITELIST_HAIR_PATH) as f:
        whitelist_hair = json.load(f)

    # Get sequences
    sequences = get_sequences(c, grouptype, subject_animations, SMPLX_NPZ_ANIMATION_FOLDER)

    index = 0
    print("Index,Type,Body,X,Y,Z,Yaw,Pitch,Roll,Comment")
    comment = f"bodies_min={c.bodies_min};bodies_max={c.bodies_max};x_offset={c.x_offset};y_offset={c.y_offset};z_offset={c.z_offset};x_min={c.x_min};x_max={c.x_max};y_min={c.y_min};y_max={c.y_max};yaw_min={c.yaw_min};yaw_max={c.yaw_max}"
    print("%d,Comment,None,0,0,0,0,0,0,%s" % (index, comment))
    index = index + 1

    total_frames = 0

    # Ensure equal use of hair types over all sequences by not using hair from previous sequences if possible.
    current_hair = { 'f':[], 'm':[] }

    for (sequence_name, subject_location_data) in sequences:
        sequence_frames = subject_location_data[0].used_frames
        total_frames += sequence_frames

        comment = f"sequence_name={sequence_name};frames={sequence_frames}"

        if hdris is not None:
            # Add HDRI name to sequence information
            hdri_name = hdris[hdris_index]
            hdris_index = (hdris_index + 1) % len(hdris)
            comment += f";hdri={hdri_name}"

        if c.override_cameraroot_location:
            comment += f";cameraroot_x={c.x_offset};cameraroot_y={c.y_offset};cameraroot_z={c.z_offset}"

        if c.camera_hfov_deg > 0:
            comment += f";camera_hfov={c.camera_hfov_deg}"

        print(f"{index},Group,None,0.0,0.0,{c.camera_height + c.z_offset},0.0,0.0,0.0,{comment}")
        index = index + 1

        current_textures_body_female = []
        current_textures_body_male = []

        for data in subject_location_data:
            comment = f"start_frame={data.start_frame}"

            # Randomize body texture, use each texture only once per sequence
            gender = subject_gender[data.subject_name]
            if gender == "f":
                if len(current_textures_body_female) == 0:
                    current_textures_body_female = list(textures_body_female)
                texture_body_name = current_textures_body_female.pop(random.randrange(len(current_textures_body_female)))
            elif gender == "m":
                if len(current_textures_body_male) == 0:
                    current_textures_body_male = list(textures_body_male)
                texture_body_name = current_textures_body_male.pop(random.randrange(len(current_textures_body_male)))
            else:
                print(f"ERROR: no gender definition for subject: {data.subject_name}", file=sys.stderr)
                sys.exit(1)

            comment += f";texture_body={texture_body_name}"

            # Randomize clothing texture
            if data.subject_name in textures_clothing:
                textures = textures_clothing[data.subject_name]
                texture_clothing_name = textures[random.randrange(len(textures))]
                comment += f";texture_clothing={texture_clothing_name}"

            if c.use_hair:
                # Randomize hair
                if len(current_hair[gender]) == 0:
                    current_hair[gender] = list(whitelist_hair[gender])

                hair_name = current_hair[gender].pop(random.randrange(len(current_hair[gender])))
                comment += f";hair={hair_name}"

            body = f"{data.subject_name}_{data.animation_name}"
            print(f"{index},Body,{body},{data.x + c.x_offset},{data.y + c.y_offset},{c.z_offset},{data.yaw},0.0,0.0,{comment}")

            index = index + 1

    print(f"[INFO] Total frames in sequences: {total_frames}", file=sys.stderr)
