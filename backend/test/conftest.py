import pytest
import json
import os

from core.models import Task

@pytest.fixture
def load_json_data():
    """Fixture para cargar datos de prueba desde archivos JSON en backend/test/data/"""
    def _load(filename):
        base_path = os.path.dirname(__file__)
        path = os.path.join(base_path, "data", filename)
        with open(path, "r") as f:
            data = json.load(f)
        
        # Convertimos la lista de tareas en objetos Task
        data["tasks_objects"] = [Task(t["name"], t["time"]) for t in data["tasks"]]
        return data
    return _load

@pytest.fixture
def small_case(load_json_data):
    """Fixture específica para el caso pequeño."""
    return load_json_data("small.json")

@pytest.fixture
def medium_case(load_json_data):
    """Fixture específica para el caso mediano."""
    return load_json_data("medium.json")

@pytest.fixture
def large_case(load_json_data):
    """Fixture específica para el caso grande."""
    return load_json_data("large.json")
