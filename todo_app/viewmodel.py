from datetime import datetime, timedelta

class ViewModel:
    def __init__(self, tasks):
        self._tasks = tasks

    @property
    def tasks(self):
        return self._tasks

    @property
    def not_started(self):
        return [task for task in self._tasks if task.status == "Not started"]
        
    @property
    def in_progress(self):
        return [task for task in self._tasks if task.status == "In progress"]

    @property
    def done(self):
        return [task for task in self._tasks if task.status == "Completed"]

    @property
    def should_show_all_done_tasks(self):
        now_in_iso = datetime.now().isoformat()
        return [task for task in self._tasks if task.status == "Completed" if task.last_modified < now_in_iso ]

    @property
    def recent_done_tasks(self): #By recent I mean completed in last 24h
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        yesterday_in_iso = yesterday.isoformat()
        return [task for task in self._tasks if task.status == "Completed" if task.last_modified > yesterday_in_iso ]

#NOT USED IN MY LOGIC ATM

    # @property
    # def older_done_tasks(self):
    #     now = datetime.now()
    #     yesterday = now - timedelta(days=1)
    #     yesterday_in_iso = yesterday.isoformat()
    #     return [task for task in self._tasks if task.status == "Completed" if task.last_modified < yesterday_in_iso ]