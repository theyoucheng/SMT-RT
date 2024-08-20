import sys

TASKS_NUM = '5'
M = '2'
K = '5'

def read_taskset(taskset_file):
    with open(taskset_file, 'r') as file:
        data = file.read()
    # Remove unwanted characters
    data = data.strip('{}').replace('False', 'false').replace('True', 'true')
    # Split data into lines and remove empty lines
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
        file.write("#define TASKS_NUM "+TASKS_NUM+"\n")
        file.write("#define M "+M+"\n")
        file.write("#define K "+K+"\n")
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
        if i == int(TASKS_NUM) - 1: 
            SIMULATION_TIME = (int(K) + 1) * int(parts[2])
        
    return SIMULATION_TIME

def main():

    taskset_index = str(sys.argv[1])

    taskset_file = "./task/taskset"+taskset_index+".txt"
    taskh = "task.h"

    # Read task data from txt file
    lines1 = read_taskset(taskset_file)
    
    SIMULATION_TIME = sim_time(lines1)

    print("simulation_time = "+str(SIMULATION_TIME))

    tasks2 = generate_tasks(lines1)

    write_taskh(taskh, tasks2, SIMULATION_TIME)

if __name__ == "__main__":
    main()