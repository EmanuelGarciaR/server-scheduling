import os
import time
from .models import Task, Server, ScheduleResult

# Use relative imports inside the package to avoid ModuleNotFoundError when running tests from different directories
from backend.algorithms.greedy import greedy
from backend.algorithms.backtracking import backtracking
from backend.algorithms.brute_force import brute_force
from backend.algorithms.divide_conquer import divide_conquer
from backend.algorithms.recursive import recursive

class CircularDependencyError(Exception):
    pass

class ValidationError(Exception):
    pass

ALGORITHMS = {
    'greedy': greedy,
    'backtracking': backtracking,
    'brute_force': brute_force,
    'divide_conquer': divide_conquer,
    'recursive': recursive
}

def validate_dependencies(raw_tasks):
    # Map all valid task IDs
    valid_ids = set()
    for task in raw_tasks:
        task_id = task.get("id")
        if task_id is None:
            raise ValidationError("Task missing 'id' property.")
        valid_ids.add(task_id)

    # 1. Dependency exists constraint
    for task in raw_tasks:
        pred_id = task.get("predecessor_id")
        if pred_id is not None and pred_id not in valid_ids:
            raise ValidationError(f"Task '{task['id']}' references a non-existent predecessor_id '{pred_id}'.")

    # 2. Circular reference constraint
    # We trace paths for each task. Since it's a single dependency structure, each task has at most one predecessor.
    visited = set()
    for task in raw_tasks:
        if task["id"] in visited:
            continue
        
        path = set()
        current_id = task["id"]
        
        while current_id is not None:
            if current_id in path:
                raise CircularDependencyError(f"Circular dependency detected involving task '{current_id}'.")
            if current_id in visited:
                # Connected to an acyclic path
                break
                
            path.add(current_id)
            visited.add(current_id)
            
            # Find the predecessor
            current_task = next((t for t in raw_tasks if t["id"] == current_id), None)
            current_id = current_task.get("predecessor_id") if current_task else None

def calculate_dependency_levels(raw_tasks):
    # Lookup dict to easily find tasks
    task_dict = {t["id"]: t for t in raw_tasks}
    
    # Memoization for calculated levels
    levels = {}
    
    def get_level(task_id):
        if task_id in levels:
            return levels[task_id]
        
        task = task_dict[task_id]
        pred_id = task.get("predecessor_id")
        
        if pred_id is None:
            levels[task_id] = 0
        else:
            levels[task_id] = get_level(pred_id) + 1
            
        return levels[task_id]

    for task in raw_tasks:
        task["dependency_level"] = get_level(task["id"])

def run_scheduler(raw_data, algorithm_name, num_servers=None):
    if not isinstance(raw_data, dict):
        raise TypeError("raw_data must be a dictionary.")
        
    raw_tasks = raw_data.get("tasks", [])
    
    if not isinstance(raw_tasks, list):
        raise TypeError("tasks must be a list in raw_data payload.")

    # Validation
    validate_dependencies(raw_tasks)

    # Pre-processing
    calculate_dependency_levels(raw_tasks)
    
    # Sort Ascending by dependency_level
    raw_tasks.sort(key=lambda t: t["dependency_level"])
    
    # Object Hydration
    if num_servers is None:
        # num_servers = getattr(raw_data, "num_servers", os.cpu_count() or 4)
        num_servers = raw_data.get("num_servers", os.cpu_count() or 4)
    if isinstance(num_servers, str):
        num_servers = int(num_servers)

    servers = [Server(server_name=f"Server-{i+1}", server_capacity=float('inf')) for i in range(num_servers)]
    
    tasks = [Task.from_json(raw_task) for raw_task in raw_tasks]

    # Dispatching
    algo_func = ALGORITHMS.get(algorithm_name)
    if not algo_func:
        raise ValueError(f"Algorithm '{algorithm_name}' is not supported. Supported: {list(ALGORITHMS.keys())}")
        
    # Execution & Benchmarking
    start_time = time.perf_counter()
    algo_func(tasks, servers)
    end_time = time.perf_counter()
    
    computation_time = end_time - start_time
    
    # Unified Payload
    return ScheduleResult(servers=servers, execution_time=computation_time)
