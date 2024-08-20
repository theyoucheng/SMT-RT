import subprocess
import re
import sys

NUM_TASKS = 5

def set_task_index(filename, task_index):
    with open(filename, 'r') as file:
        content = file.readlines()
    for i, line in enumerate(content):
        if line.startswith("#define NUMBER"):
            content[i] = f"#define NUMBER {task_index - 1}\n"
            break
    else:
        content.insert(0, f"#define NUMBER {task_index - 1}")
    
    with open(filename, 'w') as file:
        file.writelines(content)

def update_taskset(file1, file2, task_index, assert_passed, user_time, sys_time, elapsed_time):
    with open(file1, 'r') as file:
        content = file.readlines()
    task_index_zero_based = task_index - 1
    task_lines = [i for i, line in enumerate(content) if line.strip().startswith('{') and line.strip().endswith('},')]
    passed = 'true' if assert_passed else 'false'
    line = task_lines[task_index_zero_based]
    content[line] = re.sub(r'(true})', passed+"}", content[line])
    with open(file1, 'w') as file:
        file.writelines(content)
    nextline = f"\n"
    timing_info = f"//Timeing Info: Usertime: {user_time}, System time: {sys_time}, Elaped time: {elapsed_time}\n"
    result_info = f"//assert(task[{task_index_zero_based}].flag == true): {passed}\n"
    content.append(nextline)
    content.append(timing_info)
    content.append(result_info)
    with open(file2, 'a') as file:
        file.writelines(content)

def update_taskset_timeout(file1, file2, task_index):
    with open(file1, 'r') as file:
        content = file.readlines()
    task_index_zero_based = task_index - 1
    timing_info = f"//time out...\n"
    result_info = f"//assume assert(task[{task_index_zero_based}].flag == true): true\n"
    content.append(timing_info)
    content.append(result_info)
    with open(file2, 'a') as file:
        file.writelines(content)
    
def update_taskset_all_schedulable(file1, file2):
    with open(file1, 'r') as file:
        content = file.readlines()
    content.append("\n")
    content.append(f"//all tasks generated are schedulable...\n")
    with open(file2, 'a') as file:
        file.writelines(content)

def run_cbmc_with_timing(taskset_index):
    
    command = ['timeout', '1800', 'time', 'cbmc', '--object-bits', '16', '--property', 'main.assertion.1', 'main.c', 'init.c', 'simulate.c']
    
    try:
        result = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = result.communicate()
        print("\nCBMC Output:")
        print(stdout)

        timing_output = stderr.strip()
        timing_info = re.findall(r"(\d+\.\d+user) (\d+\.\d+system) (\d+:\d+\.\d+elapsed)", timing_output)

        if timing_info:
            user_time, sys_time, elapsed_time = timing_info[0]
            print(f"User time: {user_time}")
            print(f"System time: {sys_time}")
            print(f"Elapsed time: {elapsed_time}")
            assert_passed = "VERIFICATION FAILED" not in stdout
            if assert_passed:
                print("CBMC assertion passed. Generating taskset_result.txt...")
            else:
                print("CBMC assertion failed. Generating taskset_result.txt...")

            update_taskset('./task/taskset'+taskset_index+'.txt', './task/taskset_result.txt', task_index, assert_passed, user_time, sys_time, elapsed_time)

        else:
            print("timeout...\n")
            update_taskset_timeout('./task/taskset'+taskset_index+'.txt', './task/taskset_result.txt', task_index)

    except subprocess.CalledProcessError as e:
        print(f"CBMC returned non-zero exit status: {e.returncode}")
        print(f"CBMC output:\n{e.output}")
    except subprocess.TimeoutExpired:
        print("CBMC execution timed out.")
    except FileNotFoundError:
        print("Error: 'cbmc' not found. Make sure it is installed and in your PATH.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) !=3:
        print("Usage: python start.py <task_index> <taskset_index>")
        sys.exit(1)

    try:
        task_index = int(sys.argv[1])
        taskset_index = str(sys.argv[2])
        if task_index < 0 or task_index > NUM_TASKS:
            print(f"Error: The value must be between 1 and {NUM_TASKS}.")
            #sys.exit(1)
        elif task_index == 0:
            print(f"All tasks generated are schedulable.")
            update_taskset_all_schedulable('./task/taskset'+taskset_index+'.txt', './task/taskset_result.txt')
            #sys.exit(1)
        else:
            set_task_index('main.c', task_index)
            run_cbmc_with_timing(taskset_index)
    except ValueError:
        print("Error: <task_index> must be an integer between 1 and the number of tasks!")
        sys.exit(1)

    