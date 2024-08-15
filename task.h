// task.h
#ifndef TASK_H
#define TASK_H

#include <stdbool.h>

#define SIMULATION_TIME 76
#define TASKS_NUM 5
#define M 1
#define K 3
typedef struct {
    int id;
    int wcet;
    int period;
    int deadline;
    bool schedulable;
    int remaining;
    int nextStart;
    int activation;
    int abDeadline;
    int count;
    bool flag;
} Task;

extern Task tasks[TASKS_NUM];

Task tasks[TASKS_NUM] = {
    {1,1,8,3,true,1,0,0,0,0,true},
    {2,2,8,5,true,2,0,0,0,0,true},
    {3,3,14,9,true,3,0,0,0,0,true},
    {4,2,19,12,true,2,0,0,0,0,true},
    {5,1,19,12,true,1,0,0,0,0,true},
    };

void init();

#endif

