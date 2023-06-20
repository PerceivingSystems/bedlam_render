#!/usr/bin/env python
# Copyright (c) 2023 Max Planck Society
# License: https://bedlam.is.tuebingen.mpg.de/license.html
#
# Batch import clothing .abc animations into Unreal using multiprocessing
#
# Notes:
# + Python for Windows: py -3 import_abc_clothing_batch.py 1000 12
#

from multiprocessing import Pool
from pathlib import Path
import subprocess
import sys
import time

# Globals
UNREAL_APP_PATH = r"C:\UE\UE_5.0\Engine\Binaries\Win64\UnrealEditor-Cmd.exe"
UNREAL_PROJECT_PATH = r"C:\UEProjects\5.0\Sandbox5\Sandbox5.uproject"
IMPORT_SCRIPT_PATH = "C:/bedlam_render/unreal/import/import_abc_clothing.py" # need forward slashes when calling via -ExecutePythonScript

def worker(unreal_app_path, unreal_project_path, import_script_path, batch_index, num_batches):
    # "C:\UE\UE_5.0\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" "C:\UEProjects\5.0\Sandbox5\Sandbox5.uproject" -stdout -FullStdOutLogOutput -ExecutePythonScript="C:/bedlam_render/unreal/import/import_abc_smplx.py 0 10" > log-0.txt
    subprocess_args = [unreal_app_path, unreal_project_path, f"-ExecutePythonScript={import_script_path} {batch_index} {num_batches}"]
    print(subprocess_args)
    subprocess.run(subprocess_args)
    return True

def worker_args(args):
    return worker(*args)

################################################################################
# Main
################################################################################
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Usage: %s NUM_BATCHES PROCESSES' % (sys.argv[0]), file=sys.stderr)
        sys.exit(1)

    num_batches = int(sys.argv[1])
    processes = int(sys.argv[2])

    print(f"Starting pool with {processes} processes, batches: {num_batches}\n", file=sys.stderr)
    pool = Pool(processes)

    start_time = time.perf_counter()
    tasklist = []    
    for batch_index in range(num_batches):
        tasklist.append( (UNREAL_APP_PATH, UNREAL_PROJECT_PATH, IMPORT_SCRIPT_PATH, batch_index, num_batches) )

    result = pool.map(worker_args, tasklist)

    print(f"Finished. Total batch conversion time: {(time.perf_counter() - start_time):.1f}s")
