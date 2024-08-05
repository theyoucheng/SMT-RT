// task.h
#ifndef TASK_H
#define TASK_H

#include <stdbool.h>

#define SIMULATION_TIME 64
#define TASKS_NUM 5
#define M 1
#define K 3
#define NUMBER 4

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
    {1,1,6,1,true,1,0,0,0,0,true},
    {2,1,8,2,true,1,0,0,0,0,true},
    {3,1,10,10,true,1,0,0,0,0,true},
    {4,1,14,11,true,1,0,0,0,0,true},
    {5,4,16,6,false,4,0,0,0,0,true},
    };

void init();

#endif

