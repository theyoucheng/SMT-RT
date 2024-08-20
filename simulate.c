// simulate.c
#include <stdio.h>
#include "task.h"  
#include <stdbool.h>
#include <assert.h>

void simulate(int taskId) { //taskId: the index of a task in tasks; to check the task whose deadline misses if it satisfies the (m,k) constraint.
    
    //job-continue strategy: continue the job execution until completion even if its dealine is missed.

    int time = 0;
    int exTask = TASKS_NUM; //the index of the task that are running 
    int execution; //execution=1 cpu is occupied； execution=0 cpu idle
    int deadlineMiss[K];
    for(int i=0; i<K; i++){
        deadlineMiss[i]=0;    
    }
    
    while (time < SIMULATION_TIME) {

        execution = 0; //When execution equals 0, cpu is idling; When execution equals 1, there is a task executing.

        for (int i = 0; i < TASKS_NUM; i++) { //choosing a task to execute. 
            if (tasks[i].nextStart <= time && tasks[i].remaining > 0 && i <= exTask) {
                exTask = i;
                execution = 1;
                break;
            }
        }
        
        if (execution == 1) {

            tasks[exTask].remaining--;

            if(tasks[exTask].remaining == 0){
                
                if(exTask == taskId){

                    int deadlineMissCount = 0;

                    if(time > tasks[exTask].abDeadline){
                        deadlineMiss[tasks[exTask].count%K]=1;
                    }else{
                        deadlineMiss[tasks[exTask].count%K]=0;
                    }

                    for(int i=0; i<K; i++){
                        deadlineMissCount += deadlineMiss[i];
                    }
                    
                    if(deadlineMissCount > M){
                        tasks[exTask].flag=false;
                        break;
                    }

                } 
                
                tasks[exTask].count++;
                tasks[exTask].nextStart += tasks[exTask].period;
                tasks[exTask].abDeadline += tasks[exTask].period;
                tasks[exTask].remaining = tasks[exTask].wcet;
                exTask = TASKS_NUM;
            }

        }else {
            exTask = TASKS_NUM;
        }
        time++;
    }
}