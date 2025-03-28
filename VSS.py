import pandas as pd
import numpy as np
import sys
import random
from math import log

K = 1.036 # Confidence level of 85% (see https://en.wikipedia.org/wiki/Standard_normal_table)

class Task:
    def __init__(self, name, wcet, bcet, period, deadline, priority):
        self.name = name  # Task identifier
        self.wcet = wcet  # Worst-case execution time
        self.bcet = bcet  # Best-case execution time
        self.rcet = 0 # Randed-case execution time
        self.period = period  # Period of the task
        self.deadline = deadline  # Deadline for the task
        self.priority = priority  # Lower value means higher priority
        self.worst_response = 0  # Worst-case response time
        self.remaining_time = 0 # Remaining time
        self.release_time = 0 # When the task gets ready
        self.generator = np.random.default_rng()
        self.set_random_execution_time()
    
    def __repr__(self):
        return f"Task({self.name}, WCET={self.wcet}, BCET={self.bcet}, Remaining={self.remaining_time}, Priority={self.priority})"

    def set_random_execution_time(self):
        """Generate random execution time between BCET and WCET."""

        if self.wcet != self.bcet:
            self.mean = log(self.wcet - self.bcet)/2  # Mean of the lognormal distribution
            self.sigma = log(self.wcet - self.bcet)/(2*K)  # Standard deviation of the lognormal distribution

            # when bcet = 0 and wcet = 1 lognormal always returns 1 - I'm not sure if that's a mistake
            # can process take no time? Should we skip that one? Makes no sense to me @Simon
            self.rcet = self.wcet
            self.rcet = self.wcet + 1
            while self.rcet > self.wcet:
                self.rcet = self.bcet + self.generator.lognormal(mean=self.mean, sigma=self.sigma)

        else:
            self.rcet = self.bcet
        
        self.remaining_time = self.rcet


def get_ready_tasks(task_list, current_time):
    """Return tasks that are ready for execution."""
    return [task for task in task_list if task.release_time <= current_time]

def highest_priority_task(ready_tasks):
    """Return the highest priority task."""
    return min(ready_tasks, key=lambda task: task.priority) if ready_tasks else None

def advance_time():
    """Define time increment."""
    return 1

def simulate(n, tasks):
    current_time = 0

    while current_time < n and get_ready_tasks(tasks, current_time):
        ready_tasks = get_ready_tasks(tasks, current_time)
        current_task = highest_priority_task(ready_tasks)

        if current_task:
            if current_task.rcet > 0:
                """If execution time of the task equals 0, don't advance"""
                dt = advance_time()
                current_time += dt
                current_task.remaining_time -= dt

            if current_task.remaining_time <= 0:
                response_time = current_time - current_task.release_time
                current_task.worst_response = max(current_task.worst_response, response_time)
                current_task.release_time += current_task.period
                current_task.set_random_execution_time()
        else:
            current_time += advance_time()

    dict = {}
    tasks = sorted(tasks, key=lambda task: task.priority)
    for task in tasks:
        dict[task.name] = task.worst_response
    return(current_time - 1, dict)

def load_tasks_from_csv(file_path):
    df = pd.read_csv(file_path)
    tasks = [Task(row['Task'], row['WCET'], row['BCET'], row['Period'], row['Deadline'], row['Priority']) for _, row in df.iterrows()]
    return tasks

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python VSS.py <path_to_csv> <simulation_time>")
        sys.exit(1)
    file_path = sys.argv[1]
    generator = np.random.default_rng()
    tasks = load_tasks_from_csv(file_path)
    simulation_time = int(sys.argv[2])
    time, dict = simulate(simulation_time, tasks)
    print(f'Simulation time: {time}, {dict}')