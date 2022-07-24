from todo_app.data.mongoDB_items import Task
from todo_app.viewmodel import ViewModel
from datetime import datetime, timedelta

def test_completed_task_on_completed_list():
    tasks = [
        Task(0, 'Test Task', 'Task description', 'Completed', '2022-02-01T00:00:00.000Z', '2022-02-01T13:21:34.123Z' )
    ]
    completed_tasks = ViewModel(tasks).done
    assert len(completed_tasks) == 1

def test_started_task_on_in_progress_list():
    tasks = [
        Task(0, 'Test Task', 'Task description', 'In progress', '2022-02-01T00:00:00.000Z', '2022-02-01T13:21:34.123Z' )
    ]
    in_progress_tasks = ViewModel(tasks).in_progress
    assert len(in_progress_tasks) == 1

def test_not_started_task_on_not_started_list():
    tasks = [
        Task(0, 'Test Task', 'Task description', 'Not started', '2022-02-01T00:00:00.000Z', '2022-02-01T13:21:34.123Z' )
    ]
    not_started_tasks = ViewModel(tasks).not_started
    assert len(not_started_tasks) == 1

def test_show_all_completed():
    tasks = [
        Task(0, 'Test Task0', 'Task description0', 'Completed', '2022-02-01T00:00:00.000Z', '2022-02-03T13:21:34.123Z' ),
        Task(1, 'Test Task1', 'Task description1', 'Completed', '2022-02-01T00:00:00.000Z', '2022-02-02T13:21:34.123Z' ),
        Task(2, 'Test Task2', 'Task description2', 'Completed', '2022-02-01T00:00:00.000Z', '2022-02-01T13:21:34.123Z' ),
        Task(3, 'Test Task3', 'Task description3', 'Completed', '2022-02-01T00:00:00.000Z', '2022-01-31T13:21:34.123Z' ),
        Task(4, 'Test Task4', 'Task description4', 'Completed', '2022-02-01T00:00:00.000Z', '2022-01-30T13:21:34.123Z' ),
        Task(5, 'Test Task5', 'Task description5', 'Completed', '2022-02-01T00:00:00.000Z', '2022-01-29T13:21:34.123Z' ),
        Task(6, 'Test Task6', 'Task description6', 'Completed', '2022-02-01T00:00:00.000Z', '2022-01-28T13:21:34.123Z' ),
        Task(7, 'Test Task7', 'Task description7', 'Completed', '2022-02-01T00:00:00.000Z', '2022-01-27T13:21:34.123Z' )
    ]

    all_completed_tasks = ViewModel(tasks)
    assert len(all_completed_tasks.should_show_all_done_tasks) == 8

def test_show_recent_completed():
    now = datetime.now()
    now_in_iso = datetime.now().isoformat()
    n_days_ago = now - timedelta(days=3) # days = n days ago
    n_days_ago_in_iso = n_days_ago.isoformat()
    tasks = [
        Task(0, 'Test Task0', 'Task description0', 'Completed', '2022-02-01T00:00:00.000Z', now_in_iso ),
        Task(1, 'Test Task1', 'Task description1', 'Completed', '2022-02-01T00:00:00.000Z', n_days_ago_in_iso ) #3 days ago
    ]

    all_completed_tasks = ViewModel(tasks)
    assert len(all_completed_tasks.recent_done_tasks) == 1

