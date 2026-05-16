import pytest
from backend.core.sheduler import run_scheduler, CircularDependencyError, ValidationError
import os

def test_run_scheduler_circular_dependency():
    raw_data = {
        "tasks": [
            {"id": "A", "task_name": "Task A", "task_time": 10, "predecessor_id": "B"},
            {"id": "B", "task_name": "Task B", "task_time": 20, "predecessor_id": "A"}
        ]
    }
    with pytest.raises(CircularDependencyError):
        run_scheduler(raw_data, "greedy", 2)

def test_run_scheduler_non_existent_predecessor():
    raw_data = {
        "tasks": [
            {"id": "A", "task_name": "Task A", "task_time": 10, "predecessor_id": "Unknown"}
        ]
    }
    with pytest.raises(ValidationError):
        run_scheduler(raw_data, "greedy", 2)

def test_run_scheduler_success_levels():
    import backend.core.sheduler as scheduler_module
    
    # manual mock
    captured_tasks = []
    
    def dummy_algo(tasks, servers):
        captured_tasks.extend(tasks)

    # Backup and replace
    original_algorithms = scheduler_module.ALGORITHMS.copy()
    scheduler_module.ALGORITHMS['dummy'] = dummy_algo
    
    raw_data = {
        "tasks": [
            {"id": "C", "task_name": "Task C", "task_time": 10, "predecessor_id": "B"},
            {"id": "A", "task_name": "Task A", "task_time": 20, "predecessor_id": None},
            {"id": "B", "task_name": "Task B", "task_time": 30, "predecessor_id": "A"}
        ]
    }
    
    try:
        result = run_scheduler(raw_data, "dummy", 2)
        assert result.execution_time >= 0
        
        tasks_passed = captured_tasks
        
        # Validation task sorts: Level A=0, B=1, C=2
        assert tasks_passed[0].get_id() == "A"
        assert tasks_passed[0].dependency_level == 0
        
        assert tasks_passed[1].get_id() == "B"
        assert tasks_passed[1].dependency_level == 1
        
        assert tasks_passed[2].get_id() == "C"
        assert tasks_passed[2].dependency_level == 2
    finally:
        scheduler_module.ALGORITHMS = original_algorithms
