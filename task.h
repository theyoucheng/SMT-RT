// task.h
#ifndef TASK_H
#define TASK_H

#include <stdbool.h>

#define SIMULATION_TIME 76
#define TASKS_NUM 10
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
    {1,1,5,1,true,1,0,0,0,0,true},
    {2,1,6,1,false,1,0,0,0,0,true},
    {3,2,10,4,true,2,0,0,0,0,true},
    {4,1,12,4,false,1,0,0,0,0,true},
    {5,1,15,2,false,1,0,0,0,0,true},
    {6,1,16,6,false,1,0,0,0,0,true},
    {7,3,18,11,false,3,0,0,0,0,true},
    {8,1,18,7,false,1,0,0,0,0,true},
    {9,1,19,13,false,1,0,0,0,0,true},
    {10,1,19,10,false,1,0,0,0,0,true},
    };

void init();

#endif

