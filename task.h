// task.h
#ifndef TASK_H
#define TASK_H

#include <stdbool.h>

#define SIMULATION_TIME 114
#define TASKS_NUM 5
#define M 2
#define K 5
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
    {1,3,7,5,true,3,0,0,0,0,true},
    {2,1,7,5,true,1,0,0,0,0,true},
    {3,3,11,5,false,3,0,0,0,0,true},
    {4,1,13,7,false,1,0,0,0,0,true},
    {5,1,19,12,false,1,0,0,0,0,true},
    };

void init();

#endif

