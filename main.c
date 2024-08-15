#define NUMBER 4
#include <stdio.h>
#include "task.h"      // 任务结构体和外部变量的声明
#include "simulate.h"  // simulate 函数的声明
#include <assert.h>

int main() {

    init();
    
    simulate(NUMBER);
    assert(tasks[NUMBER].flag==true);

    return 0;
}
