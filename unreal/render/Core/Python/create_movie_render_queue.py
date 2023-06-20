# Copyright (c) 2023 Max Planck Society
# License: https://bedlam.is.tuebingen.mpg.de/license.html
# 
# Generates MovieRenderQueue render jobs for selected Content Browser LevelSequences
#
# Requirements: 
#   Unreal 5.0.3+
#   Plugins: 
#     + Python Editor Script Plugin
#     + Movie Render Queue
#     + Movie Render Queue Additional Render Passes (for segmentation masks)
#
import sys
import unreal

# Globals
preview_mode = False
output_dir = r"C:\bedlam\images\test"

def add_render_job(pipeline_queue, level_sequence, output_frame_step, use_tsr):
	global preview_mode
	global output_dir

	level_sequence_name = level_sequence.get_name()
	# Create new movie pipeline job and set job parameters
	job = pipeline_queue.allocate_new_job(unreal.MoviePipelineExecutorJob)
	job.set_editor_property('job_name', level_sequence_name)
	job.set_editor_property('sequence', unreal.SoftObjectPath(level_sequence.get_path_name()))

	current_level = unreal.EditorLevelUtils.get_levels(unreal.EditorLevelLibrary.get_editor_world())[0]
	map_path = unreal.SystemLibrary.get_path_name(unreal.SystemLibrary.get_outer_object(current_level))
	job.set_editor_property('map', unreal.SoftObjectPath(map_path))

	job.set_editor_property('author', "BEDLAM")

	# Add deferred rendering
	deferred_setting = job.get_configuration().find_or_add_setting_by_class(unreal.MoviePipelineDeferredPassBase)

	# Set output type PNG
	jpg_setting = job.get_configuration().find_setting_by_class(unreal.MoviePipelineImageSequenceOutput_JPG)
	if jpg_setting is not None:
		job.get_configuration().remove_setting(jpg_setting)
	job.get_configuration().find_or_add_setting_by_class(unreal.MoviePipelineImageSequenceOutput_PNG)

	output_setting = job.get_configuration().find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)

	output_directory = output_dir + "\\png\\{sequence_name}"
	file_name_format = "{sequence_name}_{frame_number}"

	if preview_mode:
		output_directory += "_preview"
		file_name_format += "_preview"

	output_setting.output_directory = unreal.DirectoryPath(output_directory)
	output_setting.file_name_format = file_name_format

	if preview_mode:
		output_setting.output_resolution = unreal.IntPoint(640, 360)
	else:
		output_setting.output_resolution = unreal.IntPoint(1280, 720)

	output_setting.zero_pad_frame_numbers = 4
	output_setting.output_frame_step = output_frame_step

	# Anti-aliasing
	antialiasing_setting = job.get_configuration().find_or_add_setting_by_class(unreal.MoviePipelineAntiAliasingSetting)

	if preview_mode:
		antialiasing_setting.spatial_sample_count = 1
		antialiasing_setting.temporal_sample_count = 1
	else:
		antialiasing_setting.spatial_sample_count = 1

		# Use 7 temporal samples instead of 8 to get sample on keyframe for default frame center shutter mode
		# https://dev.epicgames.com/community/learning/tutorials/GxdV/unreal-engine-demystifying-sampling-in-movie-render-queue
		antialiasing_setting.temporal_sample_count = 7

	antialiasing_setting.override_anti_aliasing = True

	if use_tsr:
		antialiasing_setting.anti_aliasing_method = unreal.AntiAliasingMethod.AAM_TSR
	else:
		antialiasing_setting.anti_aliasing_method = unreal.AntiAliasingMethod.AAM_NONE

	# Ensure proper Lumen warmup at frame 0, especially when rendering with frame skipping (6 fps)
	antialiasing_setting.render_warm_up_frames = True
	antialiasing_setting.engine_warm_up_count = 32

# Setup exr render job for generating depth map and segmentation masks
def add_render_job_exr(pipeline_queue, level_sequence, output_frame_step):
	global preview_mode
	global output_dir

	level_sequence_name = level_sequence.get_name()
	# Create new movie pipeline job and set job parameters
	job = pipeline_queue.allocate_new_job(unreal.MoviePipelineExecutorJob)
	job.set_editor_property('job_name', level_sequence_name + "_exr")
	job.set_editor_property('sequence', unreal.SoftObjectPath(level_sequence.get_path_name()))

	current_level = unreal.EditorLevelUtils.get_levels(unreal.EditorLevelLibrary.get_editor_world())[0]
	map_path = unreal.SystemLibrary.get_path_name(unreal.SystemLibrary.get_outer_object(current_level))
	job.set_editor_property('map', unreal.SoftObjectPath(map_path))

	job.set_editor_property('author', "BEDLAM")

	# Set output type EXR
	jpg_setting = job.get_configuration().find_setting_by_class(unreal.MoviePipelineImageSequenceOutput_JPG)
	if jpg_setting is not None:
		job.get_configuration().remove_setting(jpg_setting)

	exr_setting = job.get_configuration().find_or_add_setting_by_class(unreal.MoviePipelineImageSequenceOutput_EXR)
	exr_setting.compression = unreal.EXRCompressionFormat.ZIP # ZIP results in better compression than PIZ when including segmentation masks (ObjectIds)
	exr_setting.multilayer = True

	output_setting = job.get_configuration().find_or_add_setting_by_class(unreal.MoviePipelineOutputSetting)

	output_directory = output_dir + "\\exr\\{sequence_name}"
	file_name_format = "{sequence_name}_{frame_number}"

	if preview_mode:
		output_directory += "_preview"
		file_name_format += "_preview"

	output_setting.output_directory = unreal.DirectoryPath(output_directory)
	output_setting.file_name_format = file_name_format

	if preview_mode:
		output_setting.output_resolution = unreal.IntPoint(640, 360)
	else:
		output_setting.output_resolution = unreal.IntPoint(1280, 720)

	output_setting.zero_pad_frame_numbers = 4
	output_setting.output_frame_step = output_frame_step

	# Anti-aliasing: Disable for depth/mask rendering
	antialiasing_setting = job.get_configuration().find_or_add_setting_by_class(unreal.MoviePipelineAntiAliasingSetting)

	antialiasing_setting.spatial_sample_count = 1
	antialiasing_setting.temporal_sample_count = 1
	antialiasing_setting.override_anti_aliasing = True
	antialiasing_setting.anti_aliasing_method = unreal.AntiAliasingMethod.AAM_NONE

	# Ensure proper Lumen warmup at frame 0, especially when rendering with frame skipping (6 fps)
	antialiasing_setting.render_warm_up_frames = True
	antialiasing_setting.engine_warm_up_count = 32

	# Deferred renderer
	deferred_setting = job.get_configuration().find_or_add_setting_by_class(unreal.MoviePipelineDeferredPassBase)

	# Depth and motion vectors
	deferred_setting.use32_bit_post_process_materials = True # export 32-bit float depth
	world_depth = deferred_setting.additional_post_process_materials[0]
	world_depth.enabled = True
	deferred_setting.additional_post_process_materials[0] = world_depth
	motion_vectors = deferred_setting.additional_post_process_materials[1]
	motion_vectors.enabled = True
	deferred_setting.additional_post_process_materials[1] = motion_vectors

	# Segmentation mask (Object ID) render setup
	deferred_setting.disable_multisample_effects = True
	objectid_setting = job.get_configuration().find_or_add_setting_by_class(unreal.MoviePipelineObjectIdRenderPass)
	objectid_setting.id_type = unreal.MoviePipelineObjectIdPassIdType.LAYER

###############################################################################
# Main
###############################################################################
if __name__ == '__main__':

	unreal.log('BEDLAM: Setup Movie Render Queue render jobs for selected level sequences')

	if len(sys.argv) >= 2:
		output_dir = sys.argv[1]

	output_frame_step = 1
	use_tsr = False
	generate_exr = False

	if len(sys.argv) >= 3:
		values = sys.argv[2].split("_")
		output_frame_step = int(values[0])
		if "TSR" in values:
			use_tsr = True

		if "DepthMask" in values:
			generate_exr = True # generate depth map and segmentation masks in .exr file (separate render pass)


	# Setup movie render queue
	subsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
	pipeline_queue = subsystem.get_queue()

	if len(pipeline_queue.get_jobs()) > 0:
		# Remove all existing pipeline jobs
		for job in pipeline_queue.get_jobs():
			pipeline_queue.delete_job(job)

	selection = unreal.EditorUtilityLibrary.get_selected_assets() # Loads all selected assets into memory
	for asset in selection:
		if not isinstance(asset, unreal.LevelSequence):
			unreal.log_error(f"  Ignoring (no LevelSequence): {asset.get_full_name()}")
			continue

		level_sequence = asset
		unreal.log(f"  Adding: {level_sequence.get_full_name()}")

		add_render_job(pipeline_queue, level_sequence, output_frame_step, use_tsr)
		if generate_exr:
			# Render depth and segmentation masks into multilayer EXR file
			add_render_job_exr(pipeline_queue, level_sequence, output_frame_step)

