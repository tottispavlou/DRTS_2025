from VSS import *

RTA_values = {'T1': 1, 'T3': 2, 'T4': 4, 'T5': 6, 'T6': 10, 'T7': 28, 'T2': 54}

i = 0
max_time = 0
while(True):
    i += 1
    file_path = "Exercise/exercise-TC1.csv"
    tasks = load_tasks_from_csv(file_path)
    simulation_time = 540
    sim_time, dict = simulate(simulation_time, tasks)
    max_time = max(sim_time, max_time)
    print(max_time, i)
    if max_time >= RTA_values["T2"]:
        print(i, dict)
        break