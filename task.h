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
    {1,4,11,7,true,4,0,0,0,0,true},
    {2,1,12,9,true,1,0,0,0,0,true},
    {3,5,16,15,true,5,0,0,0,0,true},
    {4,1,20,15,true,1,0,0,0,0,true},
    {5,1,20,4,false,1,0,0,0,0,true},
    };

void init();

#endif

