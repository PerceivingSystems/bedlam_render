# Render Sequence Generation
BEDLAM Unreal render setup utilizes a data-driven design approach where external data files (`be_seq.csv`) are used to define the setup of the required Unreal assets for rendering.
The files in this folder are used to generate and modify these files.

The generated body scene data definition files will later be used by the Unreal automation tool to generate the required Unreal Sequencer `LevelSequence` assets for rendering.

# Scripts

## Generate initial scene definition
+ [be_generate_sequences_crowd.py](be_generate_sequences_crowd.py)
  + Run from WSL2 Python 3.10 venv
    + Dependencies: opencv-python-headless, numpy
  + Adjust animation folder data path at top of script
+ Generate external body scene description (`be_seq.csv`) with desired number of animated sequences. Each sequence is randomized based on predefined randomization settings for
  +  Bodies per scene
  +  Body start locations and orientations
  +  Animation subsequences
  +  Body textures
  +  Simulated clothing and textures
  +  HDR image (for IBL rendering)
+ Place randomized animated bodies on flat virtual performance stage. 
+ Utilize simple binary ground occupancy masks to avoid overlap of animated bodies. See paper for details.
+ Body and camera pose information is in standard Unreal coordinate notation
  + [cm], X: forward, Y: right, Z: up
  + Rotations: Yaw (local=global) -> Pitch (local) -> Roll (local)
    + Rotation directions:
      + yaw: positive yaw rotates to the right (left-hand rule)
      + pitch: positive pitch rotates up (right-hand rule)
      + roll: positive roll rotates clockwise (right-hand rule)
  + Default camera direction: looking along +X axis
+ Ground trajectory images for generated sequence will be stored in `images/` subfolder

### Example
```
mkdir -p /mnt/c/bedlam/images/test

# 5 people, 10 sequences
./be_generate_sequences_crowd.py be_5_10 | tee /mnt/c/bedlam/images/test/be_seq.csv

# 5 people, 10 sequences, HDR image information for IBL rendering
./be_generate_sequences_crowd.py be_5_10 ../../config/whitelist_hdri.txt | tee /mnt/c/bedlam/images/test/be_seq_hdri.csv
```

## Modify existing scene definition
+ [be_modify_sequences.py](be_modify_sequences.py)
+ Modifies existing `be_seq.csv` body scene definition with desired option
  + Randomize static camera between sequences
  + Randomize camera root yaw for randomized viewpoint onto scene
  + Replace simulated clothing with clothing overlay textures or add them

### Example
```
# Randomize static camera pose for each sequence
./be_modify_sequences.py /mnt/c/bedlam/images/test/be_seq.csv camera cam_random_c
```
