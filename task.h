// task.h
#ifndef TASK_H
#define TASK_H

#include <stdbool.h>

#define SIMULATION_TIME 64
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
    {1,1,7,4,true,1,0,0,0,0,true},
    {2,1,13,6,true,1,0,0,0,0,true},
    {3,5,14,14,true,5,0,0,0,0,true},
    {4,2,15,8,false,2,0,0,0,0,true},
    {5,3,16,6,false,3,0,0,0,0,true},
    };

void init();

#endif

