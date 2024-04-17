# Unreal Rendering
BEDLAM Unreal image rendering tools utilize Python editor scripting in combination with a custom BEDLAM Unreal Editor UI to automate the following tasks:
+ Auto-generate Unreal Sequencer `LevelSequence` assets based on selected body scene data definition file (`be_seq.csv`)
+ Setup [Movie Render Queue](https://docs.unrealengine.com/5.0/en-US/render-cinematics-in-unreal-engine/) render jobs for selected `Level Sequence` assets.
    + DX12 rasterizer with 7 temporal samples for motion blur
    + If depth maps and segmentation masks are desired a second optional render pass will be setup to output EXR files (32-bit float, multilayer, cryptomatte) without spatial and temporal samples
+ Start render and log camera ground truth poses in Unreal coordinates during rendering

BEDLAM rendering works with vanilla Unreal Editor 5.0.3 release. Unreal source code modifications or custom plugin installations are not needed.

# Requirements
+ Windows (10 or later)
+ Unreal Engine 5.0.3
+ Shared BEDLAM Core assets in Unreal Editor `Engine` content folder
    + Installation: 
        + Close Unreal Editor if running
        + Copy [Core](Core/) folder contents to `UE_5.0\Engine\Content\PS\Core` Engine install directory

+ Imported BEDLAM body and clothing assets under `UE_5.0\Engine\Content\PS` Engine install directory
  + `UE_5.0\Engine\Content\PS\Bedlam\SMPLX`: SMPL-X animated bodies (required)
  + `UE_5.0\Engine\Content\PS\Bedlam\Clothing`: simulated clothing and textures
  + `UE_5.0\Engine\Content\PS\Bedlam\HDRI\4k`: 4K HDR images
  + `UE_5.0\Engine\Content\PS\Meshcapade\SMPL`: body textures and materials

+ See [unreal_editor_assets.md](unreal_editor_assets.md) for asset data filesystem hierarchy details

+ Unreal Engine 5.0.3 project with the following active plugins
  + [Python Editor Script Plugin](https://docs.unrealengine.com/5.0/en-US/scripting-the-unreal-editor-using-python/)
  + Editor Scripting Utilities
  + Sequencer Scripting
  + Movie Render Queue
  + Movie Render Queue Additional Render Passes
    + only needed if you also want to generate depth maps and segmentation masks

+ Add path to `UE_5.0\Engine\Content\PS\Bedlam\Core\Python` engine folder to your project settings
    + Edit>Project Settings>Plugins>Python>Additional Paths: `../../Content/PS/Bedlam/Core/Python`

+ Recommended PC Hardware: 
  + CPU: Modern multi-core CPU with high clock speed (Intel i9-12900K)
  + GPU: NVIDIA RTX3090 or higher
  + Memory: 128GB or more
  + Storage: Fast SSD with >2TB of free space

# Usage
+ Copy `be_seq.csv` to target render folder
    + Example: `C:\bedlam\images\test\be_seq.csv`
+ Run BEDLAM Editor Utility Widget and dock it in Unreal UI if not already active
    + Make sure that "Show Engine Content" is activated in Content Browser settings
    + Select in Content Browser `/Engine/PS/Bedlam/Core/EditorScripting/BEDLAM`, right-click, Run Editor Utility Widget
+ Open target Level map
    + It is important to have the Level map open before you try to generate sequences since our LevelSequences depend on Level assets
    + Make sure that the Level contains the following actors from the BEDLAM core assets
        + `BE_CineCameraActor_Blueprint` attached to empty `BE_CameraRoot` actor
        + `BE_GroundTruthLogger`
+ Change path in BEDLAM UI to target render folder
    + Example: `C:\bedlam\images\test`
+ Click on `[Create LevelSequences]` and wait for them be created under `/Game/Bedlam/LevelSequences/`
    + Button will turn green at the end when LevelSequence generation was successful
    + Details: [create_level_sequences_csv.py](Core/Python/create_level_sequences_csv.py)
+ Select render preset
    + `1`: Render every frame (30fps image sequences)
    + `1_DepthMask`: Render every frame and also second render pass for depth maps and segmentation masks (30fps image sequences)
    + `5`: Render every fifth frame (6fps image sequences)
    + `5_DepthMask`: Render every fifth frame and also second render pass for depth maps and segmentation masks (6fps image sequences)
+ Select desired subset of LevelSequences in Content Browser
    + For 128GB systems you might want to limit this to 250 sequences when rendering simulated clothing to avoid out-of-memory errors
+ Click on `[Create MovieRenderQueue]` to create movie render jobs based on LevelSequence selection and render preset
    + Details: [create_movie_render_queue.py](Core/Python/create_movie_render_queue.py)
+ Click on `[Render (ground truth export)]` to start rendering with automated logging of camera ground truth
    + Details: [render_movie_render_queue.py](Core/Python/render_movie_render_queue.py)

# Notes
+ Hair
    + We are not allowed to release the used commercial hair assets. Please read [BEDLAM](https://bedlam.is.tuebingen.mpg.de/) paper and also supplementary materials for further details on this topic. We suggest to consider strand based hair grooms as mentioned in the paper. Please understand that we will not be able to provide support for this topic in this repo.
    + Only the render jobs with the `batch01handhair` name token used the commercial hair assets. You can re-render them without commercial hair by removing the `hair=....` token from the corresponding be_seq.csv files.

+ Camera ground truth
    + See [unreal_coordinate_system.md](unreal_coordinate_system.md) for details on the used format for representing camera ground truth intrinsics/extrinsics for each image.
