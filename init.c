// init.c
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include "task.h"  

int nondet_int_range(int min, int max) {
    int result = nondet_int();
    __CPROVER_assume(result >= min && result < max);
    return result;
}

void init(){

    int i = 0;
    for (i; i < TASKS_NUM - 1; i++)
    {
        tasks[i].activation=nondet_int_range(0,tasks[i].period);
        tasks[i].nextStart=tasks[i].activation;
        tasks[i].abDeadline=tasks[i].activation+tasks[i].deadline;
    }
    tasks[i].activation=0;
    tasks[i].nextStart=tasks[i].activation;
    tasks[i].abDeadline=tasks[i].activation+tasks[i].deadline;
}
