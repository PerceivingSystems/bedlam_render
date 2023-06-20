# Unreal Import Scripts
The various scripts in this folder help with automating BEDLAM related data import into Unreal.

# Requirements
+ Unreal Engine 5.0.3 with active [Python Editor Script Plugin](https://docs.unrealengine.com/5.0/en-US/scripting-the-unreal-editor-using-python/)

# Scripts

## Animated SMPL-X bodies
+ [import_abc_smplx_batch.py](import_abc_smplx_batch.py)
+ Use this script to batch import SMPL-X Alembic ABC files as `GeometryCache`
+ Requirements
    + Python for Windows (3.10.2 or later)
    + Blank Unreal project with active Python Editor Script Plugin (Sandbox5)
+ Usage
    + Adjust data paths at top of `import_abc_smplx_batch.py` and `import_abc_smplx.py` scripts
    + Run multiprocess batch import from Windows command prompt. The example below uses 10 simultaneous Unreal Engine instances for data import of 1000 data batches. Depending on your available CPU core count and available main memory (128GB+ recommended) you can increase or need to decrease the amount of processes. For fastest processing of BEDLAM release data make sure that you have a fast SSD with large enough space (700GB).
        + `py -3 import_abc_smplx_batch.py 1000 10`

## Simulated animated clothing
+ [import_abc_clothing_batch.py](import_abc_clothing_batch.py)
+ Use this script to batch import simulated 3D clothing files in Alembic ABC format as `Geometry Cache`
+ Requirements
    + Python for Windows (3.10.2 or later)
    + Blank Unreal project with active Python Editor Script Plugin (Sandbox5)
+ Usage
    + Adjust data paths at top of `import_abc_clothing_batch.py` and `import_abc_clothing.py` scripts
    + Run multiprocess batch import from Windows command prompt. The example below uses 10 simultaneous Unreal Engine instances for data import of 1000 data batches. Depending on your available CPU core count and available main memory (128GB+ recommended) you can increase or need to decrease the amount of processes. For fastest processing of BEDLAM release data make sure that you have a fast SSD with large enough space (1.4TB).
        + `py -3 import_abc_clothing_batch.py 1000 10`

## Body textures
+ [create_body_materials.py](create_body_materials.py)
+ Use this script to generate required `MaterialInstance` materials for imported BEDLAM body textures
+ Requirements
    + BEDLAM Unreal Core assets installed under your UE5 install directory
        + Example: `C:\UE_5.0\Engine\Content\PS\Bedlam\Core`
+ Usage
    + Adjust data paths at top of script
    + Run script via Execute Python Script

## Clothing textures
+ [import_clothing_textures.py](import_clothing_textures.py)
+ Use this script to import downloaded BEDLAM 3D clothing textures and generate required `MaterialInstance` materials for them
+ Requirements:
    + BEDLAM Unreal Core assets installed under your UE5 install directory
        + Example: `C:\UE_5.0\Engine\Content\PS\Bedlam\Core`
+ Usage
    + Adjust data paths at top of script
    + Run script via Execute Python Script

## HDR images
+ [import_hdr.py](import_hdr.py)
+ Use this script to import panoramic high-dynamic range images in HDR format for image-based lighting
    + Not needed for existing 3D environments from Unreal Marketplace
+ [List of used BEDLAM HDR images](../../config/whitelist_hdri.txt)
    + HDR Source: https://polyhaven.com/hdris
    + 4K HDR version (4096x2048)
+ Usage
    + Download desired 4K HDRI images in HDR format
    + Remove file resolution suffix from the filenames (`abandoned_church_4k.hdr` => `abandoned_church.hdr`)
        + `rename` is your friend and helper here.
    + Adjust data paths at top of script
    + Run script via Execute Python Script
    + After import disable Mipmaps for all imported HDR images
        + Bulk Edit via Property Matrix
            + LevelOfDetail>Mip Gen Settings>NoMipmaps
