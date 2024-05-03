# **A task scheduling simulator**

We implement a simple scheduler based on weakly hard scheduling method to simulate the scheduling process of multiple tasks on a single processor. The weakly hard scheduling model serves as a method for characterizing systems that can withstand certain deadline misses, which introduces (m,k) constraint to describe a task.

**(m,k) constraint**: no more than 𝑚 deadline misses must occur for any k consecutive activations of the task.

And we implemented the scheduler using the job-continue policy, which means the job will continue executing until its completion even if its deadline is missed.

To learn more about the program and results, you can visit: https://docs.google.com/document/d/1kjAe8owy8EH7FAZSFXwevnIey23nS3FH7I5syTPAGAo/edit?usp=sharing
## How to use it

We implemented the scheduler in `taskSimulator_jobContimue.c`, which simulates the scheduling process with tasks generated randomly. We also compared results with online tool Simso, and we have not found bugs so far.

```bash
# compile
gcc -o taskSimulator_jobContimue taskSimulator_jobContimue.c

# run
./taskSimulator_jobContimue
```

### Combining it with cbmc
Our purpose is to detect whether a task meets the (m,k) constraint using CBMC, so we select a set containing 5 tasks and make their activation time generate randomly. The test example is in `jobContinue_5_13_testcase.c`.

```bash
# compile
gcc -o taskSimulator_jobContimue taskSimulator_jobContimue.c

# check if the tasks meet the (1,3) constraint.
cbmc --object-bits 16 --property main.assertion.1 --property main.assertion.2 --property main.assertion.3 jobContinue_5_13_testcase.c
```
