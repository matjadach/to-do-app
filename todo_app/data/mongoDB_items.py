import pymongo
from datetime import datetime
from bson.objectid import ObjectId
import os
from dotenv import find_dotenv, load_dotenv


# file_path = find_dotenv(".env")
# load_dotenv(file_path, override=True)



class Task:
    def __init__(self, id, title, desc, status, due, last_modified=(datetime.now()).isoformat()):
        self.id = id
        self.title = title
        self.desc = desc
        self.status = status
        self.due = due
        self.last_modified = last_modified

class MongoDBTasks:
    def __init__(self):
        # Store connection string as a secret
        connection_string = os.environ.get("DB_CONNECTION_STRING")
        client = pymongo.MongoClient(connection_string)

        # Create a collection called "tasks_collection" within "tasks_db" database, use "tasks" when referencing in the code below

        db_name = os.environ.get("TASKS_DB_NAME")
        collection_name = os.environ.get("COLLECTION_NAME")
        self.tasks = client[f"{db_name}"][f"{collection_name}"]

    def get_all_tasks(self):
        tasks_list = []
        for task in self.tasks.find():
            tasks_list.append(Task(id=task["_id"], title=task["title"], desc=task["desc"], status=task["status"], due=task["due"], last_modified=task["last_modified"]))
        
        return tasks_list

    def get_task(self, id):
        id_filter = {"_id": ObjectId(id)}
        task = self.tasks.find_one(id_filter)

        return task

    def add_task(self, title, desc, due): # id will be derived during creation of Task instance
        task = {
            "title": title,
            "desc": desc,
            "status": "Not started", # Just added items are marked as 'Not started'
            "due": due,
            "last_modified": (datetime.now()).isoformat()
        }
        self.tasks.insert_one(task)

        
    def delete_task(self, id):
        id_filter = {"_id": ObjectId(id)}
        self.tasks.delete_one(id_filter)
        
    def update_task(self, id, new_title, new_desc, new_due):
        id_filter = {"_id": ObjectId(id)}
        update_task_values = {
            "$set": {
                "title": new_title,
                "desc": new_desc,
                "due": new_due,
                "last_modified": (datetime.now()).isoformat()
            }
        }
        self.tasks.update_one(id_filter, update_task_values)

    def mark_as_done(self, id):
        id_filter = {"_id": ObjectId(id)}
        update_task_values = {
            "$set": {
                "status": "Completed",
                "last_modified": (datetime.now()).isoformat()
            }
        }
        self.tasks.update_one(id_filter, update_task_values)

    def mark_as_in_progress(self, id):
        id_filter = {"_id": ObjectId(id)}
        update_task_values = {
            "$set": {
                "status": "In progress",
                "last_modified": (datetime.now()).isoformat()
            }
        }
        self.tasks.update_one(id_filter, update_task_values)

    def mark_as_not_started(self, id):
        id_filter = {"_id": ObjectId(id)}
        update_task_values = {
            "$set": {
                "status": "Not started",
                "last_modified": (datetime.now()).isoformat()
            }
        }
        self.tasks.update_one(id_filter, update_task_values)