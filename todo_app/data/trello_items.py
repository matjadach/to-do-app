import requests, os
from todo_app.flask_config import Config

### Fetch all variables specified in .env file
def load_config():
    config = Config()
    global key
    key = config.API_KEY
    global token
    token = config.API_TOKEN
    global  board_id
    board_id = config.BOARD
    global  notstarted_list
    notstarted_list = config.NOTSTARTED_LIST
    global inprogress_list
    inprogress_list = config.INPROGRESS_LIST
    global completed_list
    completed_list = config.COMPLETED_LIST


### Create Task class
class Task:
    def __init__(self, id, title, desc, status, due, last_modified):
        self.id = id
        self.title = title
        self.desc = desc
        self.status = status
        self.due = due
        self.last_modified = last_modified

    @classmethod
    def from_trello_card(cls, card, list_name):
        return cls(card["id"], card["name"], card["desc"], list_name, card["due"], card["dateLastActivity"])

### Fetch all tasks in a list
def get_tasks_in_a_list_trello(list_id):

    #Get list's name
    get_a_list_url = f"https://api.trello.com/1/lists/{list_id}?key={key}&token={token}"
    list_name = ((requests.request("GET", get_a_list_url)).json())["name"]

    #Get all cards/tasks from a list
    url = f"https://api.trello.com/1/lists/{list_id}/cards?key={key}&token={token}"
    headers = {"Accept": "application/json"}
    response = (requests.request("GET", url, headers=headers)).json()
    tasks = []
    for i in range(0, len(response)):
        task = Task.from_trello_card(response[i], list_name=list_name)
        tasks.append(task)
    return tasks

### Fetch tasks across all three lists --> It'll be a list of objects
def get_tasks_trello(lists):
    all_tasks = []
    for list in lists:
        tasks_from_one_list = get_tasks_in_a_list_trello(list)
        all_tasks.append(tasks_from_one_list)
    #Turn a list of lists into one list of all tasks
    one_list = [task for sublist in all_tasks for task in sublist]
    return one_list

### Fetch a card/task
def get_task_trello(task_id):

    #Get a card
    url = f"https://api.trello.com/1/cards/{task_id}?key={key}&token={token}"
    headers = {"Accept": "application/json"}
    response = (requests.request("GET", url, headers=headers)).json()

    #Get list's name
    list_id = response["idList"]
    get_a_list_url = f"https://api.trello.com/1/lists/{list_id}?key={key}&token={token}"
    list_name = ((requests.request("GET", get_a_list_url)).json())["name"]

    #Return task object based on info from the above
    task = Task.from_trello_card(response, list_name)
    return task


### Create a new card which displays as 'Not started'
def add_task_trello(title, desc, dueby):
    url = f"https://api.trello.com/1/lists/{notstarted_list}/cards?name={title}&desc={desc}&due={dueby}&key={key}&token={token}"
    headers = {"Accept": "application/json"}
    requests.request("POST", url, headers=headers)


### Delete card/task
def delete_task_trello(task_id):
    url = f"https://api.trello.com/1/cards/{task_id}?key={key}&token={token}"
    requests.request("DELETE", url)


### Update task / Rename it
def update_task_trello(task_id, title, desc, due):
    url = f"https://api.trello.com/1/cards/{task_id}?name={title}&desc={desc}&due={due}&key={key}&token={token}"
    headers = {"Accept": "application/json"}
    requests.request("PUT", url, headers=headers)


### Mark task as 'Done'
def mark_as_done(task_id):
    url = f"https://api.trello.com/1/cards/{task_id}?idList={completed_list}&key={key}&token={token}"
    headers = {"Accept": "application/json"}
    requests.request("PUT", url, headers=headers)


### Mark task as 'In progress'
def mark_as_in_progress(task_id):
    url = f"https://api.trello.com/1/cards/{task_id}?idList={inprogress_list}&key={key}&token={token}"
    headers = {"Accept": "application/json"}
    requests.request("PUT", url, headers=headers)


### Mark task as 'Not started'
def mark_as_not_started(task_id):
    url = f"https://api.trello.com/1/cards/{task_id}?idList={notstarted_list}&key={key}&token={token}"
    headers = {"Accept": "application/json"}
    requests.request("PUT", url, headers=headers)