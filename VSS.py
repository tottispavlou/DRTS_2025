import pandas as pd
import random
import sys

class Task:
    def __init__(self, name, wcet, bcet, period, deadline, priority):
        self.name = name  # Task identifier
        self.wcet = wcet  # Worst-case execution time
        self.bcet = bcet  # Best-case execution time
        self.remaining_time = get_random_execution_time(bcet, wcet)  # Random execution time
        self.period = period  # Period of the task
        # self.deadline = deadline  # Deadline for the task, actually useless, since for these tasks deadline = period
        self.priority = priority  # Lower value means higher priority
        self.worst_response = 0  # Worst-case response time
        self.release_time = -1  # Unset release time
        self.executions = 0  # Number of task executions
    
    def __repr__(self):
        return f"Task({self.name}, WCET={self.wcet}, BCET={self.bcet}, Remaining={self.remaining_time}, Priority={self.priority})"

def get_ready_tasks(task_list, current_time):
    """Return tasks that are ready for execution."""
    return [task for task in task_list if task.period * task.executions <= current_time]

def highest_priority_task(ready_tasks):
    """Return the highest priority task."""
    return min(ready_tasks, key=lambda task: task.priority) if ready_tasks else None

def advance_time():
    """Define time increment."""
    return 1

def get_random_execution_time(bcet, wcet):
    """Generate random execution time between BCET and WCET."""
    # Now with a simple randint, in the future we can use a more complex distribution
    return random.randint(bcet, wcet)

def simulate(n, tasks):
    current_time = 0
    
    while current_time <= n and any(task.remaining_time > 0 for task in tasks):
        ready_tasks = get_ready_tasks(tasks, current_time)
        current_task = highest_priority_task(ready_tasks)
        
        if current_task:
            if current_task.release_time == -1:
                current_task.release_time = current_time
            dt = advance_time()
            current_time += dt
            current_task.remaining_time -= dt
            
            if current_task.remaining_time <= 0:
                response_time = current_time - current_task.release_time
                current_task.worst_response = max(current_task.worst_response, response_time)
                current_task.release_time += current_task.period  # Assign new release time
                current_task.remaining_time = get_random_execution_time(current_task.bcet, current_task.wcet)  # Reset execution time
                current_task.executions += 1
                current_task.release_time = -1
        else:
            current_time += advance_time()
    
    # Compute and print worst-case response time for each task
    for task in tasks:
        if task.worst_response > 0:
            print(f"Task {task.name} WCRT: {task.worst_response}")
        else:
            print(f"Task {task.name} has no completed instances.")

def load_tasks_from_csv(file_path):
    df = pd.read_csv(file_path)
    tasks = [Task(row['Task'], row['WCET'], row['BCET'], row['Period'], row['Deadline'], row['Priority']) for _, row in df.iterrows()]
    return tasks

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python VSS.py <path_to_csv> <simulation_time>")
        sys.exit(1)
    file_path = sys.argv[1]
    random.seed(42)
    tasks = load_tasks_from_csv(file_path)
    simulation_time = int(sys.argv[2])
    simulate(simulation_time, tasks)
