import pytest
from fastapi.testclient import TestClient
from backend.api import app

client = TestClient(app)

SMALL_PAYLOAD = {
    "algorithm": "greedy",
    "num_servers": 3,
    "tasks": [
        {"id": "T1", "task_name": "T1", "task_time": 10, "predecessor_id": None, "task_priority": None},
        {"id": "T2", "task_name": "T2", "task_time": 20, "predecessor_id": None, "task_priority": None},
        {"id": "T3", "task_name": "T3", "task_time": 5,  "predecessor_id": None, "task_priority": None},
    ]
}

DEPENDENCY_PAYLOAD = {
    "algorithm": "greedy",
    "num_servers": 2,
    "tasks": [
        {"id": "A", "task_name": "Task A", "task_time": 10, "predecessor_id": None,  "task_priority": None},
        {"id": "B", "task_name": "Task B", "task_time": 15, "predecessor_id": "A",   "task_priority": None},
        {"id": "C", "task_name": "Task C", "task_time": 5,  "predecessor_id": None,  "task_priority": None},
    ]
}


class TestScheduleEndpointSuccess:

    def test_returns_200(self):
        response = client.post("/schedule", json=SMALL_PAYLOAD)
        assert response.status_code == 200

    def test_response_has_required_fields(self):
        response = client.post("/schedule", json=SMALL_PAYLOAD)
        data = response.json()
        assert "servers" in data
        assert "max_load" in data
        assert "execution_time" in data
        assert "total_tasks" in data

    def test_total_tasks_matches_input(self):
        response = client.post("/schedule", json=SMALL_PAYLOAD)
        data = response.json()
        assert data["total_tasks"] == len(SMALL_PAYLOAD["tasks"])

    def test_server_count_matches_input(self):
        response = client.post("/schedule", json=SMALL_PAYLOAD)
        data = response.json()
        assert len(data["servers"]) == SMALL_PAYLOAD["num_servers"]

    def test_max_load_positive(self):
        response = client.post("/schedule", json=SMALL_PAYLOAD)
        data = response.json()
        assert data["max_load"] > 0

    def test_execution_time_non_negative(self):
        response = client.post("/schedule", json=SMALL_PAYLOAD)
        data = response.json()
        assert data["execution_time"] >= 0

    def test_each_server_has_required_fields(self):
        response = client.post("/schedule", json=SMALL_PAYLOAD)
        data = response.json()
        for server in data["servers"]:
            assert "server_id" in server
            assert "server_name" in server
            assert "tasks" in server
            assert "total_load" in server

    def test_each_task_has_required_fields(self):
        response = client.post("/schedule", json=SMALL_PAYLOAD)
        data = response.json()
        for server in data["servers"]:
            for task in server["tasks"]:
                assert "id" in task
                assert "task_name" in task
                assert "task_time" in task
                assert "start_time" in task
                assert "finish_time" in task

    def test_finish_time_equals_start_plus_duration(self):
        response = client.post("/schedule", json=SMALL_PAYLOAD)
        data = response.json()
        for server in data["servers"]:
            for task in server["tasks"]:
                assert task["finish_time"] == task["start_time"] + task["task_time"]

    def test_no_server_exceeds_total_work(self):
        total_work = sum(t["task_time"] for t in SMALL_PAYLOAD["tasks"])
        response = client.post("/schedule", json=SMALL_PAYLOAD)
        data = response.json()
        for server in data["servers"]:
            assert server["total_load"] <= total_work


class TestScheduleEndpointAlgorithms:

    @pytest.mark.parametrize("algorithm", [
        "greedy", "backtracking", "brute_force", "recursive", "divide_conquer"
    ])
    def test_all_algorithms_return_200(self, algorithm):
        payload = {**SMALL_PAYLOAD, "algorithm": algorithm}
        response = client.post("/schedule", json=payload)
        assert response.status_code == 200

    @pytest.mark.parametrize("algorithm", [
        "greedy", "backtracking", "brute_force", "recursive", "divide_conquer"
    ])
    def test_all_algorithms_assign_all_tasks(self, algorithm):
        payload = {**SMALL_PAYLOAD, "algorithm": algorithm}
        response = client.post("/schedule", json=payload)
        data = response.json()
        assert data["total_tasks"] == len(SMALL_PAYLOAD["tasks"])

    def test_invalid_algorithm_returns_400(self):
        payload = {**SMALL_PAYLOAD, "algorithm": "invalid_algo"}
        response = client.post("/schedule", json=payload)
        assert response.status_code == 400
        assert "Value Error" in response.json()["detail"]


class TestScheduleEndpointDependencies:

    def test_dependency_respected(self):
        """B depende de A — B no puede empezar antes de que A termine."""
        response = client.post("/schedule", json=DEPENDENCY_PAYLOAD)
        data = response.json()
        all_tasks = {
            task["id"]: task
            for server in data["servers"]
            for task in server["tasks"]
        }
        task_a = all_tasks["A"]
        task_b = all_tasks["B"]
        assert task_b["start_time"] >= task_a["finish_time"]

    def test_circular_dependency_returns_400(self):
        payload = {
            "algorithm": "greedy",
            "num_servers": 2,
            "tasks": [
                {"id": "A", "task_name": "A", "task_time": 10, "predecessor_id": "B", "task_priority": None},
                {"id": "B", "task_name": "B", "task_time": 10, "predecessor_id": "A", "task_priority": None},
            ]
        }
        response = client.post("/schedule", json=payload)
        assert response.status_code == 400
        assert "Circular" in response.json()["detail"]

    def test_nonexistent_predecessor_returns_400(self):
        payload = {
            "algorithm": "greedy",
            "num_servers": 2,
            "tasks": [
                {"id": "A", "task_name": "A", "task_time": 10, "predecessor_id": "Z", "task_priority": None},
            ]
        }
        response = client.post("/schedule", json=payload)
        assert response.status_code == 400
        assert "Validation" in response.json()["detail"]


class TestScheduleEndpointValidation:

    def test_empty_tasks_returns_200(self):
        """Lista vacía es válida — no hay tareas que asignar."""
        payload = {**SMALL_PAYLOAD, "tasks": []}
        response = client.post("/schedule", json=payload)
        assert response.status_code == 200
        assert response.json()["total_tasks"] == 0

    def test_missing_tasks_field_returns_422(self):
        """Pydantic debe rechazar el request si falta el campo tasks."""
        response = client.post("/schedule", json={"algorithm": "greedy", "num_servers": 2})
        assert response.status_code == 422

    def test_missing_task_id_returns_422(self):
        payload = {
            "algorithm": "greedy",
            "num_servers": 2,
            "tasks": [
                {"task_name": "A", "task_time": 10}  # falta id
            ]
        }
        response = client.post("/schedule", json=payload)
        assert response.status_code == 422

    def test_num_servers_defaults_to_cpu_count(self):
        """Si no se pasa num_servers, debe usar el CPU count y retornar 200."""
        payload = {k: v for k, v in SMALL_PAYLOAD.items() if k != "num_servers"}
        response = client.post("/schedule", json=payload)
        assert response.status_code == 200

    def test_single_server_single_task(self):
        payload = {
            "algorithm": "greedy",
            "num_servers": 1,
            "tasks": [
                {"id": "X", "task_name": "X", "task_time": 42, "predecessor_id": None, "task_priority": None}
            ]
        }
        response = client.post("/schedule", json=payload)
        data = response.json()
        assert response.status_code == 200
        assert data["max_load"] == 42
        assert data["total_tasks"] == 1