from backend.core.sheduler import run_scheduler
import pytest

class TestGreedy:

    def test_all_tasks_assigned_small(self, small_case):
        result = run_scheduler(small_case, "greedy", small_case["num_servers"])
        assert result.total_tasks == len(small_case["tasks"])

    def test_all_tasks_assigned_medium(self, medium_case):
        result = run_scheduler(medium_case, "greedy", medium_case["num_servers"])
        assert result.total_tasks == len(medium_case["tasks"])

    def test_all_tasks_assigned_large(self, large_case):
        result = run_scheduler(large_case, "greedy", large_case["num_servers"])
        assert result.total_tasks == len(large_case["tasks"])

    def test_server_count_matches(self, small_case):
        result = run_scheduler(small_case, "greedy", small_case["num_servers"])
        assert len(result.servers) == small_case["num_servers"]

    def test_makespan_positive(self, small_case):
        result = run_scheduler(small_case, "greedy", small_case["num_servers"])
        assert result.max_load > 0

    def test_makespan_within_bounds_small(self, small_case):
        result = run_scheduler(small_case, "greedy", small_case["num_servers"])
        assert result.max_load <= small_case["expected_optimal_makespan"] * 2

    def test_makespan_within_bounds_medium(self, medium_case):
        result = run_scheduler(medium_case, "greedy", medium_case["num_servers"])
        assert result.max_load <= medium_case["expected_optimal_makespan"] * 2

    def test_load_balance_small(self, small_case):
        result = run_scheduler(small_case, "greedy", small_case["num_servers"])
        loads = [s.total_load for s in result.servers]
        max_task_time = max(t["task_time"] for t in small_case["tasks"])
        assert max(loads) - min(loads) <= max_task_time

    def test_execution_time_recorded(self, small_case):
        result = run_scheduler(small_case, "greedy", small_case["num_servers"])
        assert result.execution_time >= 0

    def test_is_fast_large(self, large_case):
        result = run_scheduler(large_case, "greedy", large_case["num_servers"])
        assert result.execution_time < 1.0

    def test_no_server_exceeds_total_work(self, small_case):
        total_work = sum(t["task_time"] for t in small_case["tasks"])
        result = run_scheduler(small_case, "greedy", small_case["num_servers"])
        for server in result.servers:
            assert server.total_load <= total_work