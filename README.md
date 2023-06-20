```
 _____ _____ ____  __    _____ _____ 
| __  |   __|    \|  |  |  _  |     |
| __ -|   __|  |  |  |__|     | | | |
|_____|_____|____/|_____|__|__|_|_|_|
 _____  _____  _____  ____   _____  _____ 
| __  ||   __||   | ||    \ |   __|| __  |
|    -||   __|| | | ||  |  ||   __||    -|
|__|__||_____||_|___||____/ |_____||__|__|
```

# BEDLAM Render Tools
This repository contains the render pipeline tools for [BEDLAM CVPR2023 paper](https://bedlam.is.tue.mpg.de). It includes automation scripts for SMPL-X data preparation in Blender, data import into Unreal Engine 5 and Unreal rendering.

If you are looking for code to train and evaluate the ML models from the paper then please visit this repository: https://github.com/pixelite1201/BEDLAM

# Render Pipeline

## Data preparation

### Data preparation for Unreal (Blender)
+ Create animated [SMPL-X](https://smpl-x.is.tue.mpg.de/) bodies (v1.1, female/male) from SMPL-X animation data files and export in Alembic ABC format. SMPL-X pose correctives are baked in the Alembic geometry cache and will be used in Unreal without any additional software requirements.
+ Details: [blender/smplx_anim_to_alembic/](blender/smplx_anim_to_alembic/)

### Data import (Unreal)
+ Import clothing and SMPL-X Alembic ABC files as `GeometryCache`
+ Import body textures and clothing overlay textures
+ Import high-dynamic range panoramic images (HDRIs) for image-based lighting
+ Details: [unreal/import/](unreal/import/)

## Render sequence generation
BEDLAM Unreal render setup utilizes a data-driven design approach where external data files (`be_seq.csv`) are used to define the setup of the required Unreal assets for rendering.

+ Generate body scene description (`be_seq.csv`) based on randomization configuration for all the sequences in the desired render job
  + Details: [tools/sequence_generation/](tools/sequence_generation/)

## Rendering (Unreal)
+ Auto-generate Unreal Sequencer `LevelSequence` assets based on selected body scene description file
+ Render generated Sequencer assets with [Movie Render Queue](https://docs.unrealengine.com/5.0/en-US/render-cinematics-in-unreal-engine/) using DX12 rasterizer with 7 temporal samples for motion blur
+ If depth maps and segmentation masks are desired a second optional render pass will output EXR files (32-bit float, multilayer, cryptomatte) without spatial and temporal samples
+ Camera ground truth poses in Unreal coordinates are generated during rendering
+ Details: [unreal/render/](unreal/render/)

## Post processing
+ Generate MP4 movies from image sequences with ffmpeg
+ Extract separate depth maps (EXR) and segmentation masks (PNG) if required EXR data is available
+ Details: [tools/post_render_pipeline/be_post_render_pipeline.sh](tools/post_render_pipeline/be_post_render_pipeline.sh)

# Requirements
+ Rendering: [Unreal Engine 5.0.3 for Windows](https://www.unrealengine.com) and good knowledge of how to use it
+ Data preparation: [Blender](https://www.blender.org) (3.2.2 or later)
+ Windows (10 or later)
    + Data preparation stage will likely also work under Linux or macOS thanks to Blender but we have not tested this and are not providing support for this option
    + Windows WSL2 subsystem for Linux with Ubuntu 22.04
    + [Python for Windows (3.10.2 or later)](https://www.python.org/downloads/windows/)
+ Recommended PC Hardware: 
  + CPU: Modern multi-core CPU with high clock speed (Intel i9-12900K)
  + GPU: NVIDIA RTX3090 or higher
  + Memory: 128GB or more
  + Storage: Fast SSD with 8TB of free space

# Notes
+ GitHub
  + We are not accepting unrequested pull requests
+ Logo: https://github.com/hermanTenuki/ASCII-Generator.site
  + Font: rectangles

# Citation
```
@inproceedings{Black_CVPR_2023,
  title = {{BEDLAM}: A Synthetic Dataset of Bodies Exhibiting Detailed Lifelike Animated Motion},
  author = {Black, Michael J. and Patel, Priyanka and Tesch, Joachim and Yang, Jinlong}, 
  booktitle = {Proceedings IEEE/CVF Conf.~on Computer Vision and Pattern Recognition (CVPR)},
  pages = {8726-8737},
  month = jun,
  year = {2023},
  month_numeric = {6}
}
```
