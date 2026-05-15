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

    def validate(self) -> bool:
        if not self.task_name or not self.task_time or self.task_time <= 0:
            return False
        if not isinstance(self.task_time, (int, float)):
            return False
        return True

    def to_json(self) -> dict:
        return {
            "id": self.__id,
            "task_name": self.task_name,
            "task_time": self.task_time
        }

