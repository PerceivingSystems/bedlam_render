# Copyright (c) 2023 Max Planck Society
# License: https://bedlam.is.tuebingen.mpg.de/license.html
#
# Batch import CLO exported Alembic .abc files into Unreal Engine
#

import math
import os
from pathlib import Path
import sys
import time
import unreal

data_root = r"C:\bedlam\material_4rendering\batch_01\clothing_abc"

#whitelist_subjects_path = r"C:\bedlam_render\config\whitelist_subjects.txt"
whitelist_subjects_path = None

data_root_unreal = "/Engine/PS/Bedlam/Clothing"

#whitelist_animations_path = r"C:\bedlam_render\config\whitelist_animations.txt"
whitelist_animations_path = None

def import_abc(data_root, data_root_unreal, current_batch, num_batches, whitelist_subjects=None, whitelist_animations=None):

    # Build import list
    import_abc_paths = sorted(Path(data_root).rglob("*.abc"))

    if current_batch is not None:
        section_length = math.ceil(len(import_abc_paths)/num_batches)
        start_index = current_batch * section_length
        end_index = start_index + section_length
        if end_index > len(import_abc_paths):
            end_index = len(import_abc_paths)
        print(f"Processing section: {current_batch}, total sections: {num_batches}, range: [{start_index}:{end_index}]")
        import_abc_paths = import_abc_paths[start_index : end_index]

    import_tasks = []
    for import_abc_path in import_abc_paths:

        if whitelist_subjects is not None:
            current_subject_name = import_abc_path.parent.parent.parent.name
            if current_subject_name not in whitelist_subjects:
                unreal.log(f"Skipping Alembic. Subject not whitelisted: {import_abc_path}")
                continue

        if whitelist_animations is not None:
            current_animation_name = import_abc_path.stem
            if current_animation_name not in whitelist_animations:
                unreal.log(f"Skipping Alembic. Animation not whitelisted: {import_abc_path}")
                continue

        unreal.log(f'Processing Alembic: {import_abc_path}')
        # unreal.log_flush() # Note: does not update editor console log

        # Example: rp_aaron_posed_002\clothing_simulations\0000\0000.abc
        uasset_folder_name = import_abc_path.parent.parent.parent.name
        uasset_folder = f"{data_root_unreal}/{uasset_folder_name}"
        uasset_name = f"{uasset_folder_name}_{import_abc_path.stem}_clo"
        uasset_path = f"{uasset_folder}/{uasset_name}"

        # Check if file is already imported
        if unreal.EditorAssetLibrary.does_asset_exist(uasset_path):
            unreal.log("  Skipping import. Already imported: " + uasset_path)
        else:
            unreal.log("  Importing: " + uasset_path)

            options = unreal.AbcImportSettings()
            options.import_type = unreal.AlembicImportType.GEOMETRY_CACHE

            # BUG (Unreal 5.0.3):
            # Importing with Python using frame_start=101 and frame_end=0 will lead to invalid last frame in sequence (last frame is same as the start frame).
            # We have to use frame_end=0 value since we don't know the exact number of frames for each file when using Unreal Python API.
            # Importing via Unreal Editor GUI (Frame Start=101, Frame End=0) will not have this issue but will have one additional frame in sequence at end.

            # Clothing simulation contains 100 warmup frames which we need to skip on import
            options.sampling_settings = unreal.AbcSamplingSettings(sampling_type=unreal.AlembicSamplingType.PER_FRAME, 
                                                                   frame_steps=1, 
                                                                   time_steps=0.0, 
                                                                   frame_start=101, 
                                                                   frame_end=0,
                                                                   skip_empty=False)            

            # Maximum quality settings
            options.geometry_cache_settings = unreal.AbcGeometryCacheSettings(flatten_tracks=True, 
                                                                              apply_constant_topology_optimizations=False, 
                                                                              motion_vectors=unreal.AbcGeometryCacheMotionVectorsImport.NO_MOTION_VECTORS, 
                                                                              optimize_index_buffers=False, 
                                                                              compressed_position_precision=0.01, 
                                                                              compressed_texture_coordinates_number_of_bits=16) # default: 10

            # Source Alembic data exported from Blender [m], apply conversion settings to convert to Unreal [cm]
            options.conversion_settings = unreal.AbcConversionSettings(preset=unreal.AbcConversionPreset.CUSTOM, flip_u=False, flip_v=True, scale=[100.0, - 100.0, 100.0], rotation=[90.0, 0.0, 0.0])

            task = unreal.AssetImportTask()
            task.set_editor_property("automated", True)
            task.set_editor_property("filename", str(import_abc_path))
            task.set_editor_property("destination_path", uasset_folder)
            task.set_editor_property("destination_name", uasset_name)
            task.set_editor_property("replace_existing", True)
            task.set_editor_property("save", True)
            task.set_editor_property("options", options)

            # Import one Alembic file at a time and save all imported assets immediately to avoid data loss on Unreal Editor crash
            import_tasks = [task]
            unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(import_tasks)
            unreal.EditorAssetLibrary.save_directory(data_root_unreal) # save imported materials and textures

######################################################################
# Main
######################################################################
if __name__ == '__main__':        
    unreal.log("============================================================")
    unreal.log("Running: %s" % __file__)

    current_batch = None
    num_batches = None
    if len(sys.argv) == 3:
        current_batch = int(sys.argv[1])
        num_batches = int(sys.argv[2])

    whitelist_subjects = None
    if whitelist_subjects_path is not None:
        with open(whitelist_subjects_path) as f:
            whitelist_subjects = f.read().splitlines()

    whitelist_animations = None
    if whitelist_animations_path is not None:
        with open(whitelist_animations_path) as f:
            whitelist_animations = f.read().splitlines()

    # Import Alembic files
    start_time = time.perf_counter()
    import_abc(data_root, data_root_unreal, current_batch, num_batches, whitelist_subjects, whitelist_animations)
    print(f"Alembic batch import finished. Total import time: {(time.perf_counter() - start_time):.1f}s")
