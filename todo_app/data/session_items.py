from flask import session

_DEFAULT_TASKS = [
    { 'id': 1, 'status': 'Not Started', 'title': 'List saved todo tasks' },
    { 'id': 2, 'status': 'Not Started', 'title': 'Allow new tasks to be added' }
]

new_tasks = []

def get_tasks():
    """
    Fetches all saved tasks from the session.

    Returns:
        list: The list of saved tasks.
    """
    return session.get('tasks', new_tasks.copy()) #no copy here?


def get_task(id):
    """
    Fetches the saved task with the specified ID.

    Args:
        id: The ID of the task.

    Returns:
        task: The saved task, or None if no tasks match the specified ID.
    """
    tasks = get_tasks()
    return next((task for task in tasks if task['id'] == int(id)), None)


def add_task(title):
    """
    Adds a new task with the specified title to the session.

    Args:
        title: The title of the task.

    Returns:
        task: The saved task.
    """
    tasks = get_tasks()

    # Determine the ID for the task based on that of the previously added task
    id = tasks[-1]['id'] + 1 if tasks else 0

    task = { 'id': id, 'title': title, 'status': 'Not Started' }

    # Add the task to the list
    tasks.append(task)
    session['tasks'] = tasks

    return task


def save_task(task):
    """
    Updates an existing task in the session. If no existing task matches the ID of the specified task, nothing is saved.

    Args:
        task: The task to save.
    """
    existing_tasks = get_tasks()
    updated_tasks = [task if task['id'] == existing_task['id'] else existing_task for existing_task in existing_tasks]

    session['tasks'] = updated_tasks

    return task
