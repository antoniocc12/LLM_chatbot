from chatbot.models import Task


class TaskFailure(Exception):
    """Celery Task Failure Exception"""
    def __init__(self, detail, *args, task=None, tb=None, **kwargs):
        if task:
            task.status = Task.ERROR
            task.current_state = "error"
            task.error = detail
            if tb:
                task.error += f"\n=========\n{tb}" if tb else ""
            task.save()
        super().__init__(task, detail, *args)
