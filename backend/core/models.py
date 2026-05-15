import uuid

class Task:
    def __init__(self, task_name, task_time):
        self.task_name = task_name
        self.task_time = task_time
        self.task_id = uuid.uuid4()

task1 = Task("Hola1", 100)
print(task1.task_id)