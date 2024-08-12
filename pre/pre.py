from task import generator

TASKS_NUM = str(generator.NUM_TASKS)
M = str(generator.M)
K = str(generator.K)

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

def write_preProcess(filename, tasks):
    with open(filename, 'w') as file:
        file.write('#include <stdio.h>\n')
        file.write('#include <stdlib.h>\n')
        file.write('#include <time.h>\n')
        file.write('#include <assert.h>\n')
        file.write('#include <math.h>\n')
        file.write('#include <stdbool.h>\n\n')
        file.write('#define TASKS_NUM '+TASKS_NUM+'\n\n')
        file.write('typedef struct {\n')
        file.write('    int id;\n')
        file.write('    int wcet;\n')
        file.write('    int period;\n')
        file.write('    int deadline;\n')
        file.write('    bool schedulable;\n')
        file.write('    int remaining;\n')
        file.write('    int nextStart;\n')
        file.write('    int activation;\n')
        file.write('    int abDeadline;\n')
        file.write('    int count;\n')
        file.write('    bool flag;\n')
        file.write('} Task;\n\n')
        file.write('void isSchedulable(Task* tasks, int i) {\n')
        file.write('    int Ri = tasks[i].wcet;\n')
        file.write('    int Ri_next = 0;\n')
        file.write('    double re;\n\n')
        file.write('    while (Ri_next <= tasks[i].deadline) {\n')
        file.write('        Ri_next = tasks[i].wcet;\n')
        file.write('        for(int h = 0; h < i; h++) {\n')
        file.write('            re = (double)Ri / (double)tasks[h].period;\n')
        file.write('            Ri_next += ceil(re) * tasks[h].wcet;\n')
        file.write('        }\n\n')
        file.write('        if (Ri_next == Ri) {\n')
        file.write('            break;\n')
        file.write('        }\n\n')
        file.write('        Ri = Ri_next;\n')
        file.write('    }\n\n')
        file.write('    if (Ri_next <= tasks[i].deadline) {\n')
        file.write('        tasks[i].schedulable = true;\n')
        file.write('        printf("task%d is schedulable; wcrt=%d <= deadline=%d\\n", tasks[i].id, Ri_next, tasks[i].deadline);\n')
        file.write('    } else {\n')
        file.write('        printf("task%d is unschedulable; wcrt=%d > deadline=%d\\n", tasks[i].id, Ri_next, tasks[i].deadline);\n')
        file.write('    }\n')
        file.write('}\n\n')
        file.write('int main() {\n')
        file.write(tasks)
        file.write('    for (int i = 0; i < TASKS_NUM; i++) {\n')
        file.write('        isSchedulable(tasks, i);\n')
        file.write('    }\n')
        file.write('    return 0;\n')
        file.write('}\n')

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

def update_task_file(filename, lines, schedulability):
    with open(filename, 'w') as file:
        file.write("{\n")
        for i, line in enumerate(lines):
            parts = line.strip('{}').split(',')
            if len(parts) < 11:
                continue
            if schedulability[i]:
                parts[4] = "true"
            else:
                parts[4] = "false"
            file.write("{" + ",".join(parts) + "\n")
            if i == int(TASKS_NUM) - 1: 
                SIMULATION_TIME = (int(K) + 1) * int(parts[2])
        file.write("};\n")
    return SIMULATION_TIME

def main():

    generator.main()

    taskset_file = "./task/taskset_init.txt"
    preProcess = "./pre/preProcess.c"
    taskh = "task.h"

    # Read task data from txt file
    lines1 = read_taskset(taskset_file)
    
    # Generate C code for task initialization
    tasks1 = generate_tasks(lines1)
    
    # Write the C code to the task.c file
    write_preProcess(preProcess, tasks1)

    # Run the C program
    import subprocess
    subprocess.run(["gcc", preProcess, "-o", "./pre/preProcess", "-lm"])
    result = subprocess.run(["./pre/preProcess"], capture_output=True, text=True)
    print(result.stdout)
    
    # Parse the output to get the updated task data
    schedulability = []
    for line1, line2 in zip(result.stdout.split("\n"), lines1):
        if 'is schedulable' in line1:
            schedulability.append(True)
        elif 'is unschedulable' in line1:
            schedulability.append(False)
    # Update the task file with the new schedulability data
    SIMULATION_TIME = update_task_file(taskset_file, lines1, schedulability)

    print("simulation_time = "+str(SIMULATION_TIME))

    lines2 = read_taskset(taskset_file)
    tasks2 = generate_tasks(lines2)

    write_taskh(taskh, tasks2, SIMULATION_TIME)

if __name__ == "__main__":
    main()