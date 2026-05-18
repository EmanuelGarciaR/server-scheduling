import json
import random
import os

def generate_test_case(num_servers: int, num_tasks: int, max_time: int = 100) -> dict:
    tasks = []
    for i in range(num_tasks):
        task_id = f"T{i}"
        task: dict = {
            "id": task_id,
            "task_name": task_id,
            "task_time": random.randint(1, max_time),
            "predecessor_id": None,
            "task_priority": None,
        }
        tasks.append(task)

    # Calcular el makespan óptimo teórico (lower bound)
    total_work = sum(t["task_time"] for t in tasks)
    max_single_task = max(t["task_time"] for t in tasks)
    expected_optimal_makespan = max(max_single_task, total_work // num_servers)

    return {
        "num_servers": num_servers,
        "expected_optimal_makespan": expected_optimal_makespan,
        "tasks": tasks
    }

def save_json(data: dict, filename: str) -> None:
    path = os.path.join("backend/test/data", filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Generado: {path}")

if __name__ == "__main__":
    os.makedirs("backend/test/data", exist_ok=True)

    random.seed(42)  # seed fija para que los JSON sean reproducibles

    save_json(generate_test_case(num_servers=3, num_tasks=5,   max_time=30),  "small.json")
    save_json(generate_test_case(num_servers=5, num_tasks=20,  max_time=100), "medium.json")
    save_json(generate_test_case(num_servers=10, num_tasks=100, max_time=100), "large.json")