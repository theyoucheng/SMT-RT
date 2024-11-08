import subprocess
import re
import os
from taskset.generator import NUM_TASKS, M, K, UTILIZATION_SUM, TASKSET_NUMBER

start_script = 'start.py'

def run_start_script( taskset_index):
    command = ['python3', start_script, str(taskset_index)]
    subprocess.run(command, check=True)

def main():
    for taskset_index in range(1, TASKSET_NUMBER+1):
        print(f"run taskset{taskset_index}.txt n=" + str(NUM_TASKS) + " U=" + str(UTILIZATION_SUM) + " for (" + str(M) + "," + str(K) + ")\n")        
        run_start_script(taskset_index)
        
if __name__ == "__main__":
    main()
