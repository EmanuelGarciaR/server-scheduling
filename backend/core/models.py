import uuid
import statistics

class Task:
    def __init__(self, task_name, task_time, task_priority=None, predecessor_id=None, task_id=None, dependency_level=0):
        self.task_name = task_name
        self.task_time = task_time
        self.priority = task_priority
        self.dependency = []
        self.predecessor_id = predecessor_id
        self.dependency_level = dependency_level
        self.__id = task_id if task_id is not None else self.__create_id()
        self.start_time = 0.0
        self.finish_time = 0.0

    def __str__(self):
        return f"Task: {self.task_name}, Time: {self.task_time}, ID: {self.__id}"

    def __create_id(self) -> str:
        return str(uuid.uuid4())

    def set_priority(self, priority):
        self.priority = priority

    @classmethod
    def from_json(cls, json):
        if not isinstance(json, dict):
            raise TypeError("Task json must be a dictionary.")

        task_name = json.get("task_name", json.get("name"))
        task_time = json.get("task_time", json.get("time"))
        task_priority = json.get("task_priority", json.get("priority"))
        predecessor_id = json.get("predecessor_id")
        task_id = json.get("id")
        dependency_level = json.get("dependency_level", 0)

        return cls(task_name, task_time, task_priority, predecessor_id, task_id, dependency_level)

    def get_id(self)-> str:
        return self.__id

    def to_json_task(self):
        return {
            "id": self.get_id(),
            "task_name": self.task_name,
            "task_time": self.task_time,
            "predecessor_id": self.predecessor_id,
            "dependency_level": self.dependency_level,
            "start_time": getattr(self, 'start_time', 0.0),
            "finish_time": getattr(self, 'finish_time', 0.0)
        }

    def __repr__(self):
        return f"Task(name='{self.task_name}', time={self.task_time})"
    
class Server:
    def __init__(self, server_name: str, server_capacity: int):
        self.__server_id = self.__create_server_id()
        self.server_name = server_name
        self.tasks = []
        self.capacity = server_capacity
        self.total_load = 0

    def __create_server_id(self) -> str:
        return str(uuid.uuid4())
    
    def get_server_id(self) -> str:
        return self.__server_id

    def add_task(self, task: Task, start_time: float = None):
        """Asigna una tarea al servidor y actualiza la carga total."""
        if start_time is None:
            start_time = self.total_load

        #Validation capacity
        if self.capacity is not None and start_time + task.task_time > self.capacity:
            raise ValueError(f"Cannot add task '{task.task_name}' to server '{self.server_name}': capacity exceeded.")
        
        task.start_time = start_time
        task.finish_time = start_time + task.task_time

        self.tasks.append(task)
        self.total_load = task.finish_time

    def remove_task(self, task: Task):
        """Elimina una tarea del servidor y actualiza la carga total."""
        if task in self.tasks:
            self.tasks.remove(task)
            if self.tasks:
                self.total_load = max(t.finish_time for t in self.tasks)
            else:
                self.total_load = 0
        else:
            raise ValueError(f"Task '{task.task_name}' not found in server '{self.server_name}'.")

    def clear(self):
        """Limpia las tareas asignadas."""
        self.tasks = []
        self.total_load = 0

    def to_json_server(self):
        return {
            "server_id": self.get_server_id(),
            "server_name": self.server_name,
            "tasks": [t.to_json_task() for t in self.tasks],
            "total_load": self.total_load
        }

    def __repr__(self):
        return f"Server(id='{self.get_server_id()}', load={self.total_load}, tasks={len(self.tasks)}, capacity={self.capacity})"

class ScheduleResult:
    def __init__(self, servers: list[Server], execution_time: float = 0.0):
        self.servers = servers
        self.execution_time = execution_time # Tiempo que tardó el algoritmo

    @property
    def max_load(self) -> int:
        """Retorna el Makespan (la carga máxima entre todos los servidores)."""
        return max((s.total_load for s in self.servers), default=0)

    @property
    def load_balancing_deviation(self) -> float:
        """Standard deviation of the final active times of all servers."""
        if not self.servers or len(self.servers) < 2:
            return 0.0
        loads = [s.total_load for s in self.servers]
        return statistics.stdev(loads)

    @property
    def total_tasks(self) -> int:
        return sum(len(s.tasks) for s in self.servers)

    def to_json_schedule_result(self):
        return {
            "servers": [s.to_json_server() for s in self.servers],
            "max_load": self.max_load,
            "load_balancing_deviation": self.load_balancing_deviation,
            "execution_time": self.execution_time,
            "total_tasks": self.total_tasks
        }

    def __repr__(self):
        return f"ScheduleResult(max_load={self.max_load}, servers={len(self.servers)})"

    def validate(self) -> bool:
        if not self.task_name or not self.task_time or self.task_time <= 0:
            return False
        if not isinstance(self.task_time, (int, float)):
            return False
        return True
