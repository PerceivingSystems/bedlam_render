# Copyright (c) 2023 Max Planck Society
# License: https://bedlam.is.tuebingen.mpg.de/license.html
# 
# Render jobs in MovieRenderQueue and generate camera ground truth (extrinsics/intrinsics) information
#
# Requirements: 
#   Python Editor Script Plugin
#   Unreal 5.0.3+
#
from pathlib import Path
import re
import sys
import unreal

# Globals
output_dir = r"C:\bedlam\images\test"

pipeline_executor = None

"""
    Summary:
        This function is called after the executor has finished
    Params:
        success - True if all jobs completed successfully.
"""
def OnQueueFinishedCallback(executor, success):
	unreal.log("Render queue completed. Success: " + str(success))
    
	# Delete our reference too so we don"t keep it alive.
	global pipeline_executor
	del pipeline_executor


"""
    Summary:
        This function is called after each individual job in the queue is finished.
        At this point, PIE has been stopped so edits you make will be applied to the
        editor world.
"""
def OnIndividualJobFinishedCallback(job, success):

    unreal.log("Individual job completed: success=" + str(success))

    # Export camera ground truth to .csv
    sequence_name = job.job_name
    export_camera_data(sequence_name)

def export_camera_data(sequence_name):

    camera_csv_dir = Path(output_dir) / "ground_truth" / "camera"
    camera_csv_dir.mkdir(parents=True, exist_ok=True)
    camera_csv_path = camera_csv_dir / f"{sequence_name}_camera.csv"

    unreal.log(f"BEDLAM: Exporting camera data: {camera_csv_path}")

    # Open project logfile to read camera parameters
    output = []
    logfile_dir = unreal.Paths.project_log_dir()
    project_path = unreal.Paths.get_project_file_path()
    (path, logfile_name, ext) = unreal.Paths.split(project_path)
    logfile_path = Path(logfile_dir) / f"{logfile_name}.log"

    with open(logfile_path, "r") as fp:
        lines = fp.readlines()
        lines.reverse()

        output = []
        for line in lines:
            line = line.rstrip()
            if "BEDLAM_CAMERA_START" in line:
                break

            match = re.search(r"BEDLAM_CAMERA:(.*)", line)
            if match:
                output.append(match.group(1))

    output.reverse()

    with open(camera_csv_path, "w") as fp:
        fp.write("name,x,y,z,yaw,pitch,roll,focal_length,sensor_width,sensor_height,hfov\n")
        for (index, line) in enumerate(output):
            match = re.search(r"(\d+),(.+)", line)
            if not match:
                unreal.log_error("Invalid camera data: " + line)
                return False

            frame = int(match.group(1))
            name = f"{sequence_name}_{frame:04d}.png"
            line = match.group(2)

            fp.write(name + "," + line + "\n")

        return True


###############################################################################
# Main
###############################################################################
if __name__ == "__main__":

    unreal.log("BEDLAM: Render jobs in MovieRenderQueue and generate camera ground truth (extrinsics/intrinsics) information")
    if len(sys.argv) == 2:
        output_dir = sys.argv[1]

	# Process queue
    movie_pipeline_queue_subsystem = unreal.get_editor_subsystem(unreal.MoviePipelineQueueSubsystem)
    pipeline_queue = movie_pipeline_queue_subsystem.get_queue()
    for job in pipeline_queue.get_jobs():
        print(f"{job}")

    # This renders the queue that the subsystem belongs with the PIE executor, mimicking Render (Local)
    pipeline_executor = movie_pipeline_queue_subsystem.render_queue_with_executor(unreal.MoviePipelinePIEExecutor)
    pipeline_executor.on_executor_finished_delegate.add_callable_unique(OnQueueFinishedCallback)
    pipeline_executor.on_individual_job_finished_delegate.add_callable_unique(OnIndividualJobFinishedCallback) # Only available on PIE Executor
