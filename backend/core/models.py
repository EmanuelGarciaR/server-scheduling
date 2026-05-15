import uuid

class Task:
    def __init__(self, task_name, task_time, task_priority=None):
        self.task_name = task_name
        self.task_time = task_time
        self.priority = task_priority
        self.dependency = []
        self.__id = self.__create_id()

    def __str__(self):
        return f"Task: {self.task_name}, Time: {self.task_time}, ID: {self.__id}"

    def __create_id(self) -> str:
        return str(uuid.uuid4())

    def set_priority(self, priority):
        self.priority = priority

    def get_id(self)-> str:
        return self.__id

    def to_json_task(self):
        return {
            "id": self.get_id(),
            "task_name": self.task_name,
            "task_time": self.task_time
        }

    def __repr__(self):
        return f"Task(name='{self.task_name}', time={self.task_time})"

class Server:
    def __init__(self, server_name: str, server_capacity: int):
        self.__server_id = self.create_server_id()
        self.server_name = server_name
        self.tasks = []
        self.capacity = server_capacity
        self.total_load = 0

    def __create_server_id(self) -> str:
        return str(uuid.uuid4())
    
    def get_server_id(self) -> str:
        return self.__server_id

    def add_task(self, task: Task):
        """Asigna una tarea al servidor y actualiza la carga total."""
        #Validation capacity
        if self.capacity is not None and self.total_load + task.task_time > self.capacity:
            raise ValueError(f"Cannot add task '{task.task_name}' to server '{self.server_name}': capacity exceeded.")
        self.tasks.append(task)
        self.total_load += task.task_time

    def remove_task(self, task: Task):
        """Elimina una tarea del servidor y actualiza la carga total."""
        if task in self.tasks:
            self.tasks.remove(task)
            self.total_load -= task.task_time
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
    def total_tasks(self) -> int:
        return sum(len(s.tasks) for s in self.servers)

    def to_json_schedule_result(self):
        return {
            "servers": [s.to_json_server() for s in self.servers],
            "max_load": self.max_load,
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
