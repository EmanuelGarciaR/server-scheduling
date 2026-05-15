import uuid

class Task:
    def __init__(self, task_name, task_time):
        self.task_name = task_name
        self.task_time = task_time
        self.__id = self.__create_id()

    def __str__(self):
        return f"Task: {self.task_name}, Time: {self.task_time}, ID: {self.__id}"

    def __create_id(self) -> str:
        return str(uuid.uuid4())

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
    def __init__(self, server_name: str):
        self.__server_id = self.create_server_id()
        self.server_name = server_name
        self.tasks = []
        self.total_load = 0

    def __create_server_id(self) -> str:
        return str(uuid.uuid4())
    
    def get_server_id(self) -> str:
        return self.__server_id

    def add_task(self, task: Task):
        """Asigna una tarea al servidor y actualiza la carga total."""
        self.tasks.append(task)
        self.total_load += task.task_time

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
        return f"Server(id='{self.get_server_id()}', load={self.total_load}, tasks={len(self.tasks)})"

