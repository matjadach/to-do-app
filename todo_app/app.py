from flask import Flask, render_template, request, redirect, url_for
from todo_app.flask_config import Config
from todo_app.data import session_items

app = Flask(__name__)
app.config.from_object(Config())


@app.route('/')
def index():
    tasks = session_items.get_tasks()
    return render_template('index.html', tasks = tasks)

@app.route("/add", methods=['POST'])
def add():
    title = request.form['Add']
    session_items.add_task(title)
    return redirect(url_for('index'))

@app.route("/done/<id>")
def done(id):
    task = session_items.get_task(id)
    task['status'] = 'Completed'
    session_items.update_task(task)
    return redirect(url_for('index'))

@app.route("/in_progress/<id>")
def in_progress(id):
    task = session_items.get_task(id)
    task['status'] = 'In progress'
    session_items.update_task(task)
    return index()

@app.route("/not_started/<id>")
def not_started(id):
    task = session_items.get_task(id)
    task['status'] = 'Not started'
    session_items.update_task(task)
    return index()

@app.route("/delete/<id>")
def delete(id):
    session_items.delete_task(id)
    return index()

@app.route("/update/<id>")
def show_update_page(id):
    task = session_items.get_task(id)
    return render_template('update.html', id = id, task = task)
    
@app.route("/update/<id>/submit", methods = ['POST'])
def update_task(id):
    id = id
    task = session_items.get_task(id)
    new_title = request.form['Update']
    task['title'] = new_title
    session_items.update_task(task)
    return index()    
    
@app.route("/sort_status")
def sort_status():
    session_items.sort_by_status()
    return index()

@app.route("/sort_desc")
def sort_desc():
    session_items.sort_by_title()
    return index()

@app.route("/sort_id")
def sort_id():
    session_items.sort_by_id()
    return index()
    
