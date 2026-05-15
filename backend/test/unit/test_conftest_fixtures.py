import pytest


def test_small_case_fixture(small_case):
    assert "num_servers" in small_case
    assert isinstance(small_case["num_servers"], int)
    assert "tasks_objects" in small_case
    assert isinstance(small_case["tasks_objects"], list)
    assert len(small_case["tasks_objects"]) == len(small_case["tasks"]) 
    for t in small_case["tasks_objects"]:
        assert hasattr(t, "task_name")
        assert hasattr(t, "task_time")


def test_load_json_data_callable(load_json_data):
    data = load_json_data("small.json")
    assert "tasks_objects" in data
    assert len(data["tasks_objects"]) == len(data["tasks"]) 


def test_medium_and_large_exist(medium_case, large_case):
    assert "num_servers" in medium_case
    assert "num_servers" in large_case
    assert len(medium_case["tasks_objects"]) > 0
    assert len(large_case["tasks_objects"]) > 0
