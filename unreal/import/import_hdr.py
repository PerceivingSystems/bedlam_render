# Copyright (c) 2023 Max Planck Society
# License: https://bedlam.is.tuebingen.mpg.de/license.html
#
# Import HDR images into Unreal Engine
#

import fnmatch
import os
import time
import unreal

data_root = r"C:\bedlam\render\hdr"

data_root_unreal = "/Engine/PS/Bedlam/HDRI/4k"

def import_textures(data_root, data_root_unreal):

    unreal.log('Importing data: ' + data_root)

    import_texture_paths = []
    for root, dirnames, filenames in os.walk(data_root):
        for filename in fnmatch.filter(filenames, '*.hdr'):
            import_texture_paths.append((root, filename))

    import_tasks = []

    for import_texture_dir, import_texture_name in import_texture_paths:
        import_texture_path = os.path.join(import_texture_dir, import_texture_name)

        # Check if texture is already imported
        texture_name = import_texture_name.replace(".hdr", "")
        texture_dir = import_texture_dir.replace(data_root, "").replace("\\", "/").lstrip("/")
        texture_dir = "%s/%s" % (data_root_unreal, texture_dir)
        texture_path = "%s/%s" % (texture_dir, texture_name)

        if unreal.EditorAssetLibrary.does_asset_exist(texture_path):
            unreal.log("  Already imported: " + texture_path)
        else:
            unreal.log("  Importing: " + texture_path)
            task = unreal.AssetImportTask()
            task.set_editor_property("filename", import_texture_path)
            task.set_editor_property("destination_path", texture_dir)
            task.set_editor_property('save', True)

            # Import one HDR at a time and save all imported assets immediately to avoid data loss on Unreal Editor crash
            import_tasks = [task]
            unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(import_tasks)
            unreal.EditorAssetLibrary.save_directory(data_root_unreal) # save imported data

    return

######################################################################
# Main
######################################################################
if __name__ == '__main__':        
    unreal.log("============================================================")
    unreal.log("Running: %s" % __file__)

    # Import HDR as texture cube into Unreal
    start_time = time.perf_counter()
    import_textures(data_root, data_root_unreal)
    print(f"HDR batch import finished. Total import time: {(time.perf_counter() - start_time):.1f}s")
