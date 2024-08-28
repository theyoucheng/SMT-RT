// task.h
#ifndef TASK_H
#define TASK_H

#include <stdbool.h>

#define SIMULATION_TIME 80
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
    {1,1,5,4,true,1,0,0,0,0,true},
    {2,1,5,3,true,1,0,0,0,0,true},
    {3,1,5,2,false,1,0,0,0,0,true},
    {4,1,6,5,true,1,0,0,0,0,true},
    {5,1,9,3,false,1,0,0,0,0,true},
    {6,1,12,4,false,1,0,0,0,0,true},
    {7,1,18,8,false,1,0,0,0,0,true},
    {8,1,19,16,false,1,0,0,0,0,true},
    {9,2,20,5,false,2,0,0,0,0,true},
    {10,5,20,15,false,5,0,0,0,0,true},
    };

void init();

#endif

