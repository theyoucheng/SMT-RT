#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <assert.h>

#define SIMULATION_TIME 50
#define UTILIZATION 1
#define TASKS_NUM 5

#define M 1
#define K 3

int hasZeroOffset = 0;

typedef struct {
    int id;
    int wcet;
    int period;
    int deadline;
    int remaining;
    int nextStart;
    int activation;
    int abDeadline;//the actual deadline
    int deadlineMiss[K];//the deadline miss window, which records how many times a task misses its deadline out of k consecutive activations
    int count;//recording how many times a task activates
    int flag;//whether a task satisfies the (m,k) constraint. flag is 0 initially
} Task;

int compare_tasks(const void* a, const void* b) {
    Task* taskA = (Task*)a;
    Task* taskB = (Task*)b;
    return taskA->period - taskB->period;
}

void initTasks(Task* tasks) {

    srand(time(NULL));

    for (int i = 0; i < TASKS_NUM; i++) {
        tasks[i].id = i + 1;
        // Randomly generated period between 10 and 25.
        tasks[i].period = (rand() % 16) + 10;
        tasks[i].wcet = (rand() % (tasks[i].period)) * UTILIZATION / 4 + 1;
        //deadline <= period
        tasks[i].deadline = 1 + rand() % tasks[i].period;
        
        tasks[i].remaining = tasks[i].wcet;
        //activation + period <= deadline
        //activate a task randomly
        tasks[i].activation = (rand() % SIMULATION_TIME) + 1;
        
        if (tasks[i].activation == 1) {
            hasZeroOffset = 1;
        }
        tasks[i].nextStart = tasks[i].activation;
        tasks[i].count = 0;
        tasks[i].flag = 0;
        for(int j=0; j<K; j++){
            tasks[i].deadlineMiss[j] = 0;
        }
        tasks[i].abDeadline = tasks[i].activation + tasks[i].deadline;
    }
    if (!hasZeroOffset) {
        //at least one task activates at t0.
        int ran = rand() % TASKS_NUM;
        tasks[ran].activation = 0;
        tasks[ran].nextStart = 0;
        tasks[ran].abDeadline = tasks[ran].activation + tasks[ran].deadline;
    }

    //sorting the tasks, the first task in the array have the highest priority.
    qsort(tasks, TASKS_NUM, sizeof(Task), compare_tasks);

    //the task with the lowest priority: WCRT>D，making at least one time deadline misses
    int WCRT = (rand() % (tasks[TASKS_NUM - 1].period)) * UTILIZATION / TASKS_NUM;
    if (WCRT <= 0) {
        tasks[TASKS_NUM - 1].deadline = 1;
        tasks[TASKS_NUM - 1].abDeadline = tasks[TASKS_NUM - 1].activation + tasks[TASKS_NUM - 1].deadline;
    }else{
        tasks[TASKS_NUM - 1].deadline = WCRT;
        tasks[TASKS_NUM - 1].abDeadline = tasks[TASKS_NUM - 1].activation + tasks[TASKS_NUM - 1].deadline;
    }
    
    for (int i = 0; i < TASKS_NUM; i++) {
        printf("Task%d wcet: %d\n", tasks[i].id, tasks[i].wcet);
        printf("Task%d period: %d\n", tasks[i].id, tasks[i].period);
        printf("Task%d deadline: %d\n", tasks[i].id, tasks[i].deadline);
        printf("Task%d activation: %d\n", tasks[i].id, tasks[i].activation);
        printf("Task%d nextStart: %d\n", tasks[i].id, tasks[i].nextStart);
        printf("Task%d remaining: %d\n", tasks[i].id, tasks[i].remaining);
    }
}

void simulate(Task* tasks) {
    
    //job-continue strategy: continue the job execution until completion even if its dealine is misses.
    int time = 0;
    int exTask = TASKS_NUM; //the index of the task that are running 
    int execution;//execution=1 cpu is occupied； execution=0 cpu idle
    
    while (time < SIMULATION_TIME) {

        execution = 0;
        for (int i = 0; i < TASKS_NUM; i++) {
            if (tasks[i].nextStart <= time && tasks[i].remaining > 0 && i <= exTask) {
                exTask = i;
                execution = 1;
            }
        }
        
        if (execution == 1) {
            printf("t%d\ttask%d\n", time, tasks[exTask].id);

            if (tasks[exTask].remaining > 0) {
                tasks[exTask].remaining--;
            
                if (tasks[exTask].remaining == 0) {
                    int deadlineMissCount = 0;//counting times of deadlinemiss in the activation window for k consecutive times
                    if(time > tasks[exTask].abDeadline){
                        tasks[exTask].deadlineMiss[tasks[exTask].count%K]=1;
                        printf("task%d deadline miss\n", tasks[exTask].id);
                    }
                    tasks[exTask].count++;
                    for(int i=0; i<K; i++){
                        deadlineMissCount += tasks[exTask].deadlineMiss[i];
                    }
                    if(deadlineMissCount > M){
                        tasks[exTask].flag = 1;//not satisfy (m,k) constraint
                    }
                    tasks[exTask].nextStart += tasks[exTask].period;
                    printf("task%d nextStart: %d\n", tasks[exTask].id, tasks[exTask].nextStart);
                    tasks[exTask].abDeadline += tasks[exTask].period;
                    printf("task%d abDeadline: %d\n", tasks[exTask].id, tasks[exTask].abDeadline);
                    tasks[exTask].remaining = tasks[exTask].wcet;
                    exTask = TASKS_NUM;
                }
            }
        }else {
            //printf("t%d\t idle\n", time);
            exTask = TASKS_NUM;
        }
        time++;
    }
}


int main() {

    int count = 0;
    srand(time(NULL));
    Task* tasks = malloc(TASKS_NUM * sizeof(Task));

    initTasks(tasks);

    simulate(tasks);

    for(int i = 0; i < TASKS_NUM; i++){
        if(tasks[i].flag == 1){
            printf("task%d does not satisfy (%d,%d) constraint.\n", tasks[i].id, M, K);
            count++;
        }
    }
    printf("job-continue(%d,%d) count:%d cnf:%f\n", M, K, count, (float)(TASKS_NUM-count)/TASKS_NUM);

    free(tasks);

    return 0;
}
