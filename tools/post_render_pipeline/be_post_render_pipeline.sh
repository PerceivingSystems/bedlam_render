#/bin/bash
# Copyright (c) 2023 Max Planck Society
# License: https://bedlam.is.tuebingen.mpg.de/license.html
#
# Post render pipeline for BEDLAM renderings
#
# 1. Remove warmup frames from rendered image folder
# 2. Generate H.264 .mp4 movies for rendered sequences
# 3. Extract depth and segmentation masks if required EXR images were generated
#
# Usage: 
# + Run from Windows WSL2 (Python 3.10)
# + `bash ./be_post_render_pipeline.sh /mnt/c/bedlam/images/myrenderjob 30`
#   + Will generate 30fps MP4 movies in landscape mode (1280x720)
# + `bash ./be_post_render_pipeline.sh /mnt/c/bedlam/images/myrenderjob 30 rotate`
#   + Will generate 30fps MP4 movies in portrait mode (720x1280)
#
# Requirements: 
# + ffmpeg (see `create_movies_from_images.py` for details`)
# + OpenEXR virtual environment (see `exr_save_depth_masks.py` for details)
#
VENV_PATH="$HOME/.virtualenvs/openexr"

echo "Usage: $0 RENDER_OUTPUT_DIRECTORY [FRAMERATE [rotate]]"

if [ -z "$1" ] ; then
    exit 1
fi

RENDER_OUTPUT_DIRECTORY=$1

FRAMERATE=30
if [ "$2" ]; then
    FRAMERATE=$2
fi

echo "Framerate: $FRAMERATE"

ROTATE=
if [ "$3" ]; then
    ROTATE="rotate"
fi

echo "Processing render directory: '$RENDER_OUTPUT_DIRECTORY'"
IMAGE_FOLDER="${RENDER_OUTPUT_DIRECTORY%/}/png/"
if [ ! -d "$IMAGE_FOLDER" ]; then
    echo "ERROR: PNG image directory not existing: '$IMAGE_FOLDER'"
    exit 1
fi

HAVE_EXR=1
EXR_FOLDER="${RENDER_OUTPUT_DIRECTORY%/}/exr/"
if [ ! -d "$EXR_FOLDER" ]; then
    echo "WARNING: EXR image directory not existing: '$EXR_FOLDER'"
    HAVE_EXR=
fi

# Delete all warmup frames (images with negative frame numbers)
echo "Deleting warmup frames: '$IMAGE_FOLDER'"
find "$IMAGE_FOLDER" -maxdepth 2 -name "*-????.png" -type f -delete

if [ -n "$HAVE_EXR" ]; then
    echo "Deleting warmup frames: '$EXR_FOLDER'"
    find "$EXR_FOLDER" -maxdepth 2 -name "*-????.exr" -type f -delete
fi

NUM_SEQUENCES=$(ls -1 $IMAGE_FOLDER | wc -l)
NUM_IMAGES=$(find $IMAGE_FOLDER -type f -name "*.png" | wc -l)
echo "Number of rendered image sequences: $NUM_SEQUENCES [Images: $NUM_IMAGES]"

if [ -n "$HAVE_EXR" ]; then
    NUM_EXR_SEQUENCES=$(ls -1 $EXR_FOLDER | wc -l)
    NUM_EXR_IMAGES=$(find $EXR_FOLDER -type f -name "*.exr" | wc -l)

    echo "Number of rendered exr sequences: $NUM_EXR_SEQUENCES [Images: $NUM_EXR_IMAGES]"
fi

read -p "Continue (y/n)?" ANSWER
if [ ! "$ANSWER" = "y" ]; then
    exit 1
fi

# Generate movies
MOVIE_FOLDER="${RENDER_OUTPUT_DIRECTORY%/}/mp4/"
echo "Generating sequence movies (H.264 .mp4): '$MOVIE_FOLDER'"
python3 ./create_movies_from_images.py "$IMAGE_FOLDER" "$MOVIE_FOLDER" $FRAMERATE $ROTATE

# Extract depth and segmentation masks from raw exr
if [ -n "$HAVE_EXR" ]; then
    EXR_CAMERA_GT_DIR="${RENDER_OUTPUT_DIRECTORY%/}/ground_truth/camera_exr"
    echo "Moving auto-generated exr camera ground truth: $EXR_CAMERA_GT_DIR"
    mkdir -p "$EXR_CAMERA_GT_DIR"
    mv ${RENDER_OUTPUT_DIRECTORY%/}/ground_truth/camera/*_exr_*.csv "$EXR_CAMERA_GT_DIR"
    echo "Extracting depth and segmentation masks"
    source "$VENV_PATH/bin/activate"
    ./exr_save_depth_masks.py "$EXR_FOLDER" "${RENDER_OUTPUT_DIRECTORY%/}/" > /dev/null
    deactivate
fi
