from models.task import Task

class TaskController:
    def __init__(self):
        pass

    def get_tasks(self):
        return Task.get_all_tasks()

    def add_task(self, title, category, priority, estimated_pomodoros):
        if not title:
            return False
        Task.add_task(title, category, priority, estimated_pomodoros)
        return True

    def delete_task(self, task_id):
        Task.delete_task(task_id)

    def toggle_task_completion(self, task_id, current_status):
        return Task.toggle_complete(task_id, current_status)
