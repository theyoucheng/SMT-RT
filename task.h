// task.h
#ifndef TASK_H
#define TASK_H

#include <stdbool.h>

#define SIMULATION_TIME 80
#define TASKS_NUM 6
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
    {1,1,5,2,true,1,0,0,0,0,true},
    {2,1,7,3,true,1,0,0,0,0,true},
    {3,1,7,6,true,1,0,0,0,0,true},
    {4,1,9,8,true,1,0,0,0,0,true},
    {5,1,18,6,true,1,0,0,0,0,true},
    {6,12,20,13,false,12,0,0,0,0,true},
    };

void init();

#endif

