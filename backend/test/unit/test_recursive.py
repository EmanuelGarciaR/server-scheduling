from backend.core.sheduler import run_scheduler

class TestRecursive:

    def test_all_tasks_assigned_small(self, small_case):
        result = run_scheduler(small_case, "recursive", small_case["num_servers"])
        assert result.total_tasks == len(small_case["tasks"])

    def test_all_tasks_assigned_medium(self, medium_case):
        result = run_scheduler(medium_case, "recursive", medium_case["num_servers"])
        assert result.total_tasks == len(medium_case["tasks"])

    def test_server_count_matches(self, small_case):
        result = run_scheduler(small_case, "recursive", small_case["num_servers"])
        assert len(result.servers) == small_case["num_servers"]

    def test_makespan_positive(self, small_case):
        result = run_scheduler(small_case, "recursive", small_case["num_servers"])
        assert result.max_load > 0

    def test_matches_brute_force_small(self, small_case):
        """Recursivo debe dar el mismo makespan que fuerza bruta."""
        bf_result = run_scheduler(small_case, "brute_force", small_case["num_servers"])
        rec_result = run_scheduler(small_case, "recursive", small_case["num_servers"])
        assert rec_result.max_load == bf_result.max_load

    def test_no_server_exceeds_total_work(self, small_case):
        total_work = sum(t["task_time"] for t in small_case["tasks"])
        result = run_scheduler(small_case, "recursive", small_case["num_servers"])
        for server in result.servers:
            assert server.total_load <= total_work

    def test_execution_time_recorded(self, small_case):
        result = run_scheduler(small_case, "recursive", small_case["num_servers"])
        assert result.execution_time >= 0