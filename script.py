import subprocess
import re
import os

# 任务集合文件路径
taskset_dir = './task'
# 要运行的脚本
start_script = 'start.py'
pre_script = 'pre.pre'

def extract_false_task_indices(taskset_file):
    false_indices = []
    with open(taskset_file, 'r') as file:
        content = file.read()
        
        # 找到每个任务集合
        tasksets = content.split('};')
        for taskset in tasksets:
            if not taskset.strip():
                continue
            # 分析任务
            tasks = taskset.strip().split('\n')
            for i, task in enumerate(tasks):
                if task.strip() and ',false' in task:
                    # 任务的索引从1开始
                    false_indices.append(i)
    return false_indices

def run_start_script(task_index, taskset_index):
    command = ['python3', start_script, str(task_index), str(taskset_index)]
    subprocess.run(command, check=True)

def run_pre_script(taskset_index):
    command = ['python3', '-m', pre_script, str(taskset_index)]
    subprocess.run(command, check=True)


def main():
    for taskset_index in range(1, 6):
        taskset_file = os.path.join(taskset_dir, f'taskset{taskset_index}.txt')
        false_indices = extract_false_task_indices(taskset_file)
        
        run_pre_script(taskset_index)
        print(f"run taskset{taskset_index}.txt\n")

        if not false_indices:
            print(f"No tasks with 'false' in taskset{taskset_index}.txt")
            run_start_script(0, taskset_index)
            continue
        
        for task_index in false_indices:
            print(f"Running start.py with task_index={task_index} and taskset_index={taskset_index}")
            run_start_script(task_index, taskset_index)
        
        # 如果 task_index 为5时，增加 taskset_index 并继续
        if taskset_index == 5:
            break

if __name__ == "__main__":
    main()
