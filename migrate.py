### Script to migrate existing tasks from Trello to MondoDB

import requests, os, pymongo
from dotenv import load_dotenv, find_dotenv

file_path = find_dotenv(".env")
load_dotenv(file_path, override=True)

### Set up for Trello.

key = os.environ.get('API_KEY')
token = os.environ.get('API_TOKEN')
lists = [os.environ.get('NOTSTARTED_LIST'), os.environ.get('INPROGRESS_LIST'), os.environ.get('COMPLETED_LIST')]

### Set up for MongoDB instance
connection_string = os.environ.get("DB_CONNECTION_STRING")
client = pymongo.MongoClient(connection_string)

db_name = os.environ.get("TASKS_DB_NAME")
collection_name = os.environ.get("COLLECTION_NAME")
tasks_mongoDB = client[f"{db_name}"][f"{collection_name}"]


def transfer_tasks(lists, delete_after_transfer):
    tasks = []

    #Get list's name
    for list_id in lists:
        get_a_list_url = f"https://api.trello.com/1/lists/{list_id}?key={key}&token={token}"
        list_name = ((requests.request("GET", get_a_list_url)).json())["name"]

        #Get all cards/tasks from a list
        url = f"https://api.trello.com/1/lists/{list_id}/cards?key={key}&token={token}"
        headers = {"Accept": "application/json"}
        response = (requests.request("GET", url, headers=headers)).json()
        for i in range(0, len(response)):
            task = {
                "title": response[i]["name"],
                "desc": response[i]["desc"],
                "status": list_name,
                "due": response[i]["due"],
                "last_modified": response[i]["dateLastActivity"]
            }
            tasks.append(task)
            if delete_after_transfer == True:
                url_to_delete_task = f"https://api.trello.com/1/cards/{(response[i]['id'])}?key={key}&token={token}"
                requests.request("DELETE", url_to_delete_task)
            else:
                continue
    return tasks

tasks_to_transfer = transfer_tasks(lists, True) #Set it to False if you wish to keep the tasks in Trello

try:
    tasks_mongoDB.insert_many(tasks_to_transfer)
except TypeError:
    print("There are no tasks to be transferred from Trello")
