import pandas as pd
import math

def load_tasks_from_csv(file_path):
    df = pd.read_csv(file_path)  
    return df.to_dict(orient='records')

def rta_test(tasks):
    tasks.sort(key=lambda x: x['Priority'])
    wcrt = {}
    
    for i, task in enumerate(tasks):
        I = 0
        while True:
            R = I + task['WCET']
            wcrt[task['Task']] = R  
            
            if R > task['Deadline']:
                return "UNSCHEDULABLE", wcrt
            
            new_I = sum(
                math.ceil(R / tasks[j]['Period']) * tasks[j]['WCET'] 
                for j in range(i)
            )
            
            if new_I == I:
                break 
            
            I = new_I
    
    return "SCHEDULABLE", wcrt

if __name__ == "__main__":
    file_path = "Exercise/exercise-TC3.csv"
    tasks = load_tasks_from_csv(file_path)
    result, wcrt = rta_test(tasks)
    print(result)
    print("Worst-case response times:", wcrt)

