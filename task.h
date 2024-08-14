// task.h
#ifndef TASK_H
#define TASK_H

#include <stdbool.h>

#define SIMULATION_TIME 80
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
    {1,1,5,3,true,1,0,0,0,0,true},
    {2,5,14,12,true,5,0,0,0,0,true},
    {3,1,15,3,false,1,0,0,0,0,true},
    {4,1,17,6,false,1,0,0,0,0,true},
    {5,2,20,19,true,2,0,0,0,0,true},
    };

void init();

#endif

