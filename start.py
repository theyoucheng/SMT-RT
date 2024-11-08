import subprocess
import re
import sys
from taskset.generator import NUM_TASKS, M, K, UTILIZATION_SUM

def read_taskset(taskset_file):
    with open(taskset_file, 'r') as file:
        data = file.read()
    data = data.strip('{}').replace('False', 'false').replace('True', 'true')
    lines = [line.strip() for line in data.split('\n') if line.strip()]
    return lines

def generate_tasks(lines):
    tasks = "Task tasks[TASKS_NUM] = {\n"
    for line in lines:
        tasks += f"    {line}\n"
    return tasks

def write_taskh(filename, tasks, SIMULATION_TIME):
    with open(filename, 'w') as file:
        file.write("// task.h\n")
        file.write("#ifndef TASK_H\n#define TASK_H\n\n")
        file.write("#include <stdbool.h>\n\n")
        file.write("#define SIMULATION_TIME "+str(SIMULATION_TIME)+"\n")
        file.write("#define TASKS_NUM "+str(NUM_TASKS)+"\n")
        file.write("#define M "+str(M)+"\n")
        file.write("#define K "+str(K)+"\n")
        file.write("typedef struct {\n")
        file.write("    int id;\n")
        file.write("    int wcet;\n")
        file.write("    int period;\n")
        file.write("    int deadline;\n")
        file.write("    bool schedulable;\n")
        file.write("    int remaining;\n")
        file.write("    int nextStart;\n")
        file.write("    int activation;\n")
        file.write("    int abDeadline;\n")
        file.write("    int count;\n")
        file.write("    bool flag;\n")
        file.write("} Task;\n\n")
        file.write("extern Task tasks[TASKS_NUM];\n\n")
        file.write(tasks)
        file.write("\n")
        file.write("void init();\n\n")
        file.write("#endif\n\n")

def sim_time(lines):
    for i, line in enumerate(lines):
        parts = line.strip('{}').split(',')
        if i == NUM_TASKS - 1: 
            SIMULATION_TIME = (int(K) + 1) * int(parts[2])
    return SIMULATION_TIME

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
    temp = "************************\n"
    taskset_info = f"Reading {file1}\n"
    with open(file1, 'r') as file:
        content = file.readlines()
    task_index_zero_based = task_index - 1
    task_lines = [i for i, line in enumerate(content) if line.strip().startswith('{') and line.strip().endswith('},')]
    passed = 'true' if assert_passed else 'false'
    line = task_lines[task_index_zero_based]
    content[line] = re.sub(r'(true})', passed+"}", content[line])
    # with open(file1, 'w') as file:
    #    file.writelines(content)
    task_info = f"task id: {task_index}, {content[task_index]}task{task_index} is un-schedulable\n"
    m_k_info =  f"Running weakly-hard analysis: M={str(M)}, K={str(K)}\n"
    timing_info = f"Timeing Info: Usertime: {user_time}, System time: {sys_time}, Elaped time: {elapsed_time}\n"
    result_info = f"Constrain satisfied? {passed}\n"
    content.append(task_info)
    content.append(m_k_info)        
    content.append(timing_info)
    content.append(result_info)
    content.append("\n")
    content.insert(0, taskset_info)
    content.insert(0, temp)
    with open(file2, 'a') as file:
        file.writelines(content)

def update_taskset_timeout(file1, file2, task_index):
    temp = "************************\n"
    taskset_info = f"Reading {file1}\n"
    with open(file1, 'r') as file:
        content = file.readlines()    
    task_info = f"task id: {task_index}, {content[task_index]}task{task_index} is un-schedulable\n"
    m_k_info =  f"Running weakly-hard analysis: M={str(M)}, K={str(K)}\n"
    timing_info = f"Timeing Info: time out ...\n"
    result_info = f"Constrain satisfied? unknown\n"
    content.append(task_info)
    content.append(m_k_info)        
    content.append(timing_info)
    content.append(result_info)
    content.append("\n")
    content.insert(0, taskset_info)
    content.insert(0, temp)
    with open(file2, 'a') as file:
        file.writelines(content)
        
def run_cbmc_with_timing(taskset_file, result_file):
    command = ['timeout', '3600', 'time', 'cbmc', '--object-bits', '16', '--property', 'main.assertion.1', 'main.c', 'init.c', 'simulate.c']
    try:
        result = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = result.communicate()
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
            update_taskset(taskset_file, result_file, task_index, assert_passed, user_time, sys_time, elapsed_time)

        else:
            print("timeout...\n")
            update_taskset_timeout(taskset_file, result_file, task_index)
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
    if len(sys.argv) !=2:
        print("Usage: python start.py <taskset_index>")
        sys.exit(1)
    try:
        task_index = NUM_TASKS
        taskset_index = str(sys.argv[1]) # 1~100
        taskset = "./taskset/n-" + str(NUM_TASKS) + "_u-" + str(UTILIZATION_SUM) + "/" + str(taskset_index) + ".txt"
        result_file = "./taskset/n-" + str(NUM_TASKS) + "_u-" + str(UTILIZATION_SUM) + "_result.txt"
        set_task_index('main.c', task_index)
        lines = read_taskset(taskset)
        print(lines)
        SIMULATION_TIME = sim_time(lines)
        tasks = generate_tasks(lines)
        write_taskh("task.h", tasks, SIMULATION_TIME)
        run_cbmc_with_timing(taskset, result_file)
    except ValueError:
        print("Error: <task_index> must be an integer between 1 and the number of tasks!")
        sys.exit(1)

    