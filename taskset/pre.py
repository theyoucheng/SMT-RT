import sys
from generator import NUM_TASKS, M as GM, K as GK, UTILIZATION_SUM, TASKSET_NUMBER
import math
import re
import generator

TASKS_NUM = str(NUM_TASKS)
M = str(GM)
K = str(GK)

class Task:
    def __init__(self, id, wcet, period, deadline, schedulable, remaining, nextStart, activation, abDeadline, count, flag):
        self.id = id
        self.wcet = wcet
        self.period = period
        self.deadline = deadline
        self.schedulable = schedulable
        self.remaining = remaining
        self.nextStart = nextStart
        self.activation = activation
        self.abDeadline = abDeadline
        self.count = count
        self.flag = flag
    def __str__(self):
        return f"{{{self.id},{self.wcet},{self.period},{self.deadline},{'true' if self.schedulable else 'false'},{self.remaining},{self.nextStart},{self.activation},{self.abDeadline},{self.count},{'true' if self.flag else 'false'}}}"


def is_schedulable(tasks, i):
    Ri = tasks[i].wcet
    Ri_next = 0
    while Ri_next <= tasks[i].deadline:
        Ri_next = tasks[i].wcet
        for h in range(i):
            re = Ri / tasks[h].period
            Ri_next += math.ceil(re) * tasks[h].wcet
        if Ri_next == Ri:
            break
        Ri = Ri_next
    if Ri_next <= tasks[i].deadline:
        tasks[i].schedulable = True
        print(f"task{tasks[i].id} is schedulable; wcrt={Ri_next} <= deadline={tasks[i].deadline}")
    else:
        print(f"task{tasks[i].id} is unschedulable; wcrt={Ri_next} > deadline={tasks[i].deadline}")

def read_taskset(filename):
    tasks = []
    with open(filename, 'r') as f:
        data = f.read()
        matches = re.findall(r'\{(.*?)\}', data)
        for match in matches:
            values = match.split(',')
            id = int(values[0])
            wcet = int(values[1])
            period = int(values[2])
            deadline = int(values[3])
            schedulable = values[4].strip().lower() == 'true'
            remaining = int(values[5])
            nextStart = int(values[6])
            activation = int(values[7])
            abDeadline = int(values[8])
            count = int(values[9])
            flag = values[10].strip().lower() == 'true'
            tasks.append(Task(id, wcet, period, deadline, schedulable, remaining, nextStart, activation, abDeadline, count, flag))
    return tasks

def write_taskset(tasks, filename):
    with open(filename, 'w') as f:
        f.write("{\n")
        for task in tasks:
            f.write(str(task) + ",\n")
        f.write("};\n")

def main():
    index = 1
    while index <= TASKSET_NUMBER:
        print(f"taskset{index}: \n")
        generator.main(index)
        filename="./taskset/n-" + TASKS_NUM + "_u-" + str(UTILIZATION_SUM) + "/" + str(index) + ".txt"
        taskset = read_taskset(filename)
        for i in range(0, NUM_TASKS):
            is_schedulable(taskset, i)
            if not taskset[i].schedulable and i != NUM_TASKS-1:
                break
            if not taskset[i].schedulable and i == NUM_TASKS-1:
                write_taskset(taskset, filename)
                index += 1
        
if __name__ == "__main__":
    main()