// task.h
#ifndef TASK_H
#define TASK_H

#include <stdbool.h>

#define SIMULATION_TIME 72
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
    {1,1,5,4,true,1,0,0,0,0,true},
    {2,1,9,3,true,1,0,0,0,0,true},
    {3,2,10,10,true,2,0,0,0,0,true},
    {4,4,14,14,true,4,0,0,0,0,true},
    {5,1,18,8,false,1,0,0,0,0,true},
    };

void init();

#endif

