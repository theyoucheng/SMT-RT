#define NUMBER 4
#include <stdio.h>
#include "task.h"      // 任务结构体和外部变量的声明
#include "simulate.h"  // simulate 函数的声明
#include "scheduler.h"
#include <assert.h>

int main() {

    init();
    Scheduler rms_scheduler = { rms_init, rms_schedule, TASKS_NUM };
    Scheduler fifo_scheduler = { fifo_init, fifo_schedule, TASKS_NUM };
    Scheduler edf_scheduler = { edf_init, edf_schedule, TASKS_NUM };
    Scheduler rr_scheduler = { rr_init, rr_schedule, TASKS_NUM };

    Scheduler* scheduler = &rms_scheduler; // &fifo_scheduler, &edf_scheduler, &rr_scheduler

    scheduler->init(scheduler, tasks);

    simulate(NUMBER, scheduler);
    assert(tasks[NUMBER].flag==true);

    return 0;
}
