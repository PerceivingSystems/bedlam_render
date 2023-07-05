# Copyright (c) 2023 Max Planck Society
# License: https://bedlam.is.tuebingen.mpg.de/license.html
#
# Generate Material Instances for selected textures
#

import os
from pathlib import Path
import sys
import time
import unreal

data_root_unreal = "/Engine/PS/Meshcapade/SMPL"
master_material_name = f"/Engine/PS/Bedlam/Core/Materials/M_SMPLX"

def create_material(master_material, texture):

    material_instance_name = f"MI_{texture.get_name()}"
    material_instance_root = f"{data_root_unreal}/Materials"
    material_instance_path = f"{material_instance_root}/{material_instance_name}"
    if unreal.EditorAssetLibrary.does_asset_exist(material_instance_path):
        unreal.log("  Skipping. MaterialInstance exists: " + material_instance_path)
        return

    unreal.log(f"Creating MaterialInstance: {material_instance_root}/{material_instance_name}")
    material_instance = unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name=material_instance_name, package_path=material_instance_root, asset_class=unreal.MaterialInstanceConstant, factory=unreal.MaterialInstanceConstantFactoryNew())
    unreal.MaterialEditingLibrary.set_material_instance_parent(material_instance, master_material)
    unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(material_instance, 'BaseColor', texture)

    return

######################################################################
# Main
######################################################################
if __name__ == "__main__":        
    unreal.log("============================================================")
    unreal.log("Running: %s" % __file__)

# Load master material
master_material = unreal.EditorAssetLibrary.load_asset(f"Material'{master_material_name}'")
if not master_material:
    unreal.log_error('Cannot load master material: ' + master_material_name)
else:
    selection = unreal.EditorUtilityLibrary.get_selected_assets() # Loads all selected assets into memory
    if len(selection) == 0:
        unreal.log_error(f"No textures selected")

    for asset in selection:
        if not isinstance(asset, unreal.Texture):
            unreal.log_error(f"  Ignoring (no Texture): {asset.get_full_name()}")
            continue

        texture = asset
        unreal.log(f"  Adding: {texture.get_full_name()}")

        create_material(master_material, texture)
