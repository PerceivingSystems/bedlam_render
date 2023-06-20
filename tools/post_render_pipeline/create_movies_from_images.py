#!/usr/bin/env python3
# Copyright (c) 2023 Max Planck Society
# License: https://bedlam.is.tuebingen.mpg.de/license.html
#
# Create movies from image sequences
#
# Requirements: ffmpeg (Tested with version 4.4.2, Ubuntu 22.04)
#

from pathlib import Path
import subprocess
import sys
import time

def make_movie(input_path, output_path, framerate, rotate):

    output_path.parent.mkdir(parents=True, exist_ok=True)

    # ffmpeg -y -framerate 30 -pattern_type glob -i "folder/*.png" -c:v libx264 -r 30 -pix_fmt yuv420p -preset slow -crf 18 output.mp4
    subprocess_args = ["ffmpeg"]
    subprocess_args.extend(["-y"]) # overwrite existing movie file
    subprocess_args.extend(["-framerate", str(framerate)])
    subprocess_args.extend(["-pattern_type", "glob"])
    subprocess_args.extend(["-i", str(input_path / "*.png")])

    if rotate:
        subprocess_args.extend(["-vf", "transpose=clock"]) # 90 deg clockwise

    subprocess_args.extend(["-c:v", "libx264"])
    subprocess_args.extend(["-r", str(framerate)])
    subprocess_args.extend(["-pix_fmt", "yuv420p"])
    subprocess_args.extend(["-preset", "slow"])
    subprocess_args.extend(["-crf", "18"])
    subprocess_args.extend([f"{output_path}"])

    subprocess.run(subprocess_args)

    return True

################################################################################
# Main
################################################################################
if __name__ == "__main__":
    if (len(sys.argv) < 4) or (len(sys.argv) > 5):
        print("Usage: %s INPUTDIR OUTPUTDIR FRAMERATE [rotate]" % (sys.argv[0]), file=sys.stderr)
        sys.exit(1)
    
    input_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    framerate = int(sys.argv[3])
    rotate = False
    if len(sys.argv) == 5:
        rotate = True

    print(f"Image input directory: {input_dir}")
    print(f"Movie output directory: {output_dir}")
    print(f"Framerate: {framerate}")
    print(f"Rotate images: {rotate}")

    start_time = time.perf_counter()

    # Get list of directories
    image_directories = sorted(input_dir.glob("**"))

    for image_directory in image_directories:
        # Skip directories without png images
        num_images = len(list(image_directory.glob("*.png")))
        if num_images == 0:
            print(f"Skipping (no images): {image_directory}")
            continue

        output_path = output_dir / image_directory.with_suffix(".mp4").name
        if output_path.exists():
            print(f"Skipping (mp4 exists): {output_path}")
            continue

        print(f"Processing: {image_directory}")
        success = make_movie(image_directory, output_path, framerate, rotate)
        if not success:
            print("ERROR! Aborting movie generation.", file=sys.stderr)
            break

    print(f"Finished. Total movie generation time: {(time.perf_counter() - start_time):.1f}s")
