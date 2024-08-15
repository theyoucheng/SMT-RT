#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <assert.h>
#include <math.h>
#include <stdbool.h>

#define TASKS_NUM 5

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

void isSchedulable(Task* tasks, int i) {
    int Ri = tasks[i].wcet;
    int Ri_next = 0;
    double re;

    while (Ri_next <= tasks[i].deadline) {
        Ri_next = tasks[i].wcet;
        for(int h = 0; h < i; h++) {
            re = (double)Ri / (double)tasks[h].period;
            Ri_next += ceil(re) * tasks[h].wcet;
        }

        if (Ri_next == Ri) {
            break;
        }

        Ri = Ri_next;
    }

    if (Ri_next <= tasks[i].deadline) {
        tasks[i].schedulable = true;
        printf("task%d is schedulable; wcrt=%d <= deadline=%d\n", tasks[i].id, Ri_next, tasks[i].deadline);
    } else {
        printf("task%d is unschedulable; wcrt=%d > deadline=%d\n", tasks[i].id, Ri_next, tasks[i].deadline);
    }
}

int main() {
Task tasks[TASKS_NUM] = {
    {1,1,8,3,false,1,0,0,0,0,true},
    {2,2,8,5,false,2,0,0,0,0,true},
    {3,3,14,9,false,3,0,0,0,0,true},
    {4,2,19,12,false,2,0,0,0,0,true},
    {5,1,19,12,false,1,0,0,0,0,true},
    };
    for (int i = 0; i < TASKS_NUM; i++) {
        isSchedulable(tasks, i);
    }
    return 0;
}
