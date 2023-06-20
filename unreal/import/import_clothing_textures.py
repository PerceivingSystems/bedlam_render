# Copyright (c) 2023 Max Planck Society
# License: https://bedlam.is.tuebingen.mpg.de/license.html
#
# Import clothing textures and generate MaterialInstances
#

import os
from pathlib import Path
import sys
import time
import unreal

DATA_ROOT = r"E:\bedlam\material_4rendering\clothing_abc"
DATA_ROOT_UNREAL = "/Engine/PS/Bedlam/Clothing/Materials"
MASTER_MATERIAL_PATH = "/Engine/PS/Bedlam/Core/Materials/M_Clothing"
def import_textures(texture_paths):

    master_material = unreal.EditorAssetLibrary.load_asset(f"Material'{MASTER_MATERIAL_PATH}'")
    if not master_material:
        unreal.log_error(f"Cannot load master material: {MASTER_MATERIAL_PATH}")
        return False

    for texture_path in texture_paths:
        unreal.log(f"Processing {texture_path}")

        # Check if texture is already imported
        # clothing_abc\rp_aaron_posed_002\clothing_textures\texture_01\texture_01_diffuse_1001.png
        subject_name = texture_path.parent.parent.parent.name
        texture_name = texture_path.parent.name

        import_tasks = []

        # Diffuse texture
        texture_asset_name = f"T_{subject_name}_{texture_name}_diffuse"
        texture_asset_dir = f"{DATA_ROOT_UNREAL}/{subject_name}"
        texture_asset_path = f"{texture_asset_dir}/{texture_asset_name}"

        if unreal.EditorAssetLibrary.does_asset_exist(texture_asset_path):
            unreal.log("  Skipping. Already imported: " + texture_asset_path)
        else:
            unreal.log("  Importing: " + texture_asset_path)
            task = unreal.AssetImportTask()
            task.set_editor_property("filename", str(texture_path))
            task.set_editor_property("destination_name", texture_asset_name)
            task.set_editor_property("destination_path", texture_asset_dir)
            task.set_editor_property('save', True)
            import_tasks.append(task)

        # Normal texture
        normal_texture_path = texture_path.parent / texture_path.name.replace("diffuse", "normal")
        normal_texture_asset_name = f"T_{subject_name}_{texture_name}_normal"
        normal_texture_asset_path = f"{texture_asset_dir}/{normal_texture_asset_name}"

        if unreal.EditorAssetLibrary.does_asset_exist(normal_texture_asset_path):
            unreal.log("  Skipping. Already imported: " + normal_texture_asset_path)
        else:
            unreal.log("  Importing: " + normal_texture_asset_path)
            task = unreal.AssetImportTask()
            task.set_editor_property("filename", str(normal_texture_path))
            task.set_editor_property("destination_name", normal_texture_asset_name)
            task.set_editor_property("destination_path", texture_asset_dir)
            task.set_editor_property('save', True)
            import_tasks.append(task)

        # Import diffuse and normal textures
        unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(import_tasks)

        # Load diffuse and normal textures
        texture_asset = unreal.EditorAssetLibrary.load_asset(f"Texture2D'{texture_asset_path}'")
        if not texture_asset:
                unreal.log_error(f"Cannot load texture: {texture_asset_path}")
                return False

        normal_texture_asset = unreal.EditorAssetLibrary.load_asset(f"Texture2D'{normal_texture_asset_path}'")
        if not texture_asset:
                unreal.log_error(f"Cannot load texture: {normal_texture_asset_path}")
                return False

        # Create MaterialInstance
        material_instance_name = f"MI_{subject_name}_{texture_name}"
        material_instance_dir = texture_asset_dir
        material_instance_path = f"{material_instance_dir}/{material_instance_name}"
        if unreal.EditorAssetLibrary.does_asset_exist(material_instance_path):
            unreal.log("  Skipping. MaterialInstance exists: " + material_instance_path)
        else:
            unreal.log(f"  Creating MaterialInstance: {material_instance_path}")
            material_instance = unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name=material_instance_name, package_path=material_instance_dir, asset_class=unreal.MaterialInstanceConstant, factory=unreal.MaterialInstanceConstantFactoryNew())
            unreal.MaterialEditingLibrary.set_material_instance_parent(material_instance, master_material)
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(material_instance, 'BaseColor', texture_asset)
            unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(material_instance, 'Normal', normal_texture_asset)

    return True

######################################################################
# Main
######################################################################
if __name__ == "__main__":        
    unreal.log("============================================================")
    unreal.log("Running: %s" % __file__)

    # Build import list
    import_texture_paths = sorted(Path(DATA_ROOT).rglob("*diffuse*.png"))

    import_textures(import_texture_paths)
