import drs
import random
from collections import namedtuple
import os

NUM_TASKS = 7
UTILIZATION_SUM = 1.0
TMIN = 5
TMAX = 20
M = 1
K = 3
TASKSET_NUMBER = 100

# Define the Task structure
Task = namedtuple('Task', ['id', 'wcet', 'period', 'deadline', 'schedulable', 'remaining', 'nextStart', 'activation', 'abDeadline', 'count', 'flag'])

def generate_tasks(num_tasks, utilization_sum, Tmin, Tmax):
    # Generate utilization vector using DRS
    utilizations = drs.drs(num_tasks, utilization_sum)
    tasks = []
    for i, utilization in enumerate(utilizations):
        id = i + 1
        period = random.randint(Tmin, Tmax) 
        wcet = max(1, int(utilization * period))  # set WCET equal to (utilization * period)
        deadline = random.randint(wcet, period)  # set deadline equal to period
        task = Task(id=id, wcet=wcet, period=period, deadline=deadline, 
                    schedulable=False, remaining=wcet, activation=0, nextStart=0,
                    abDeadline=0, count=0, flag=True)
        tasks.append(task)
    tasks.sort(key=lambda x : x.period)
    for i, task in enumerate(tasks):
        tasks[i] = task._replace(id=i + 1)
    return tasks

def write_taskset(tasks, count, num_tasks, utilization_sum):
    filename="./taskset/n-" + str(num_tasks) + "_u-" + str(utilization_sum) + "/" + str(count) + ".txt"
    dir_path = os.path.dirname(filename)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    with open(filename, "w") as file:
        file.write("{\n")
        for task in tasks:
            file.write("{"+",".join(map(str, task))+"},\n")
        file.write("};\n")

def main(index):

    num_tasks = NUM_TASKS
    utilization_sum =UTILIZATION_SUM
    Tmin = TMIN
    Tmax = TMAX
    tasks = generate_tasks(num_tasks, utilization_sum, Tmin, Tmax)
    for i, task in enumerate(tasks):
        print(f"{task.id},{task.wcet},{task.period},{task.deadline}")
    write_taskset(tasks, index, num_tasks, utilization_sum)