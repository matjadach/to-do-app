from flask import session

tasks = []



def get_tasks():
    """
    Fetches all updated tasks from the session.

    Returns:
        list: The list of updated tasks.
    """
    return session.get('tasks', tasks.copy())


def get_task(id):
    """
    Fetches the updated task with the specified ID.

    Args:
        id: The ID of the task.

    Returns:
        task: The updated task, or None if no tasks match the specified ID.
    """
    tasks = get_tasks()
    return next((task for task in tasks if task['id'] == int(id)), None)


def add_task(title):
    """
    Adds a new task with the specified title to the session.

    Args:
        title: The title of the task.

    Returns:
        task: The updated task.
    """
    tasks = get_tasks()

    # Determine the ID for the task based on that of the previously added task
    list_of_ids = [x['id'] for x in tasks]
    list_of_ids.sort()
    id = list_of_ids[-1] + 1 if tasks else 0

    task = { 'id': id, 'title': title, 'status': 'Not started' }

    # Add the task to the list
    tasks.append(task)
    session['tasks'] = tasks

    return task


def update_task(task):
    """
    Updates an existing task in the session. If no existing task matches the ID of the specified task, nothing is updated.

    Args:
        task: The task to update.
    """
    existing_tasks = get_tasks()
    updated_tasks = [task if task['id'] == existing_task['id'] else existing_task for existing_task in existing_tasks]

    session['tasks'] = updated_tasks

    return task

def delete_task(id):
    existing_tasks = get_tasks()
    updated_tasks = []
    for task in existing_tasks:
        if task['id'] != int(id):
            updated_tasks.append(task)
    session['tasks'] = updated_tasks


def sort_status_function(i):
    return i['status']

def sort_title_function(i):
    return i['title']

def sort_id_function(i):
    return i['id']

def sort_by_status():
    tasks = get_tasks()
    sorted_tasks = sorted(tasks, key=sort_status_function, reverse=True)
    session['tasks'] = sorted_tasks
    return sorted_tasks

def sort_by_title():
    tasks = get_tasks()
    sorted_tasks = sorted(tasks, key=sort_title_function)
    session['tasks'] = sorted_tasks
    return sorted_tasks

def sort_by_id():
    tasks = get_tasks()
    sorted_tasks = sorted(tasks, key=sort_id_function,)
    session['tasks'] = sorted_tasks
    return sorted_tasks

