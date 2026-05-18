from backend.core.sheduler import run_scheduler

class TestBacktracking:

    def test_all_tasks_assigned_small(self, small_case):
        result = run_scheduler(small_case, "backtracking", small_case["num_servers"])
        assert result.total_tasks == len(small_case["tasks"])

    def test_all_tasks_assigned_medium(self, medium_case):
        result = run_scheduler(medium_case, "backtracking", medium_case["num_servers"])
        assert result.total_tasks == len(medium_case["tasks"])

    def test_server_count_matches(self, small_case):
        result = run_scheduler(small_case, "backtracking", small_case["num_servers"])
        assert len(result.servers) == small_case["num_servers"]

    def test_optimal_makespan_small(self, small_case):
        """Backtracking debe encontrar el makespan óptimo exacto."""
        result = run_scheduler(small_case, "backtracking", small_case["num_servers"])
        assert result.max_load == small_case["expected_optimal_makespan"]

    def test_better_or_equal_than_greedy(self, small_case):
        greedy_result = run_scheduler(small_case, "greedy", small_case["num_servers"])
        bt_result = run_scheduler(small_case, "backtracking", small_case["num_servers"])
        assert bt_result.max_load <= greedy_result.max_load

    def test_makespan_positive(self, small_case):
        result = run_scheduler(small_case, "backtracking", small_case["num_servers"])
        assert result.max_load > 0

    def test_no_server_exceeds_total_work(self, small_case):
        total_work = sum(t["task_time"] for t in small_case["tasks"])
        result = run_scheduler(small_case, "backtracking", small_case["num_servers"])
        for server in result.servers:
            assert server.total_load <= total_work

    def test_execution_time_recorded(self, small_case):
        result = run_scheduler(small_case, "backtracking", small_case["num_servers"])
        assert result.execution_time >= 0