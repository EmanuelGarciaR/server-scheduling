import json
import random
import os

def generate_test_case(num_servers, num_tasks, max_time=100):
    tasks = [{"name": f"T{i}", "time": random.randint(1, max_time)} for i in range(num_tasks)]
    return {
        "num_servers": num_servers,
        "tasks": tasks
    }

def save_json(data, filename):
    path = os.path.join("backend/test/data", filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Generado: {path}")

if __name__ == "__main__":
    # Asegurar que el directorio existe
    os.makedirs("backend/test/data", exist_ok=True)
    
    # Medium: 5 servidores, 20 tareas
    save_json(generate_test_case(5, 20), "medium.json")
    
    # Large: 10 servidores, 100 tareas
    save_json(generate_test_case(10, 100), "large.json")
