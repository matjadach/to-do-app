from flask import Flask, render_template, request, redirect, url_for
from todo_app.flask_config import Config
from todo_app.data import trello_items
import os

app = Flask(__name__)
app.config.from_object(Config())

@app.route('/')
def index():
    all_three_lists = [os.getenv("NOTSTARTED_LIST"), os.getenv("INPROGRESS_LIST"), os.getenv("COMPLETED_LIST")]
    tasks = trello_items.get_tasks_trello(all_three_lists)
    return render_template('index.html', tasks = tasks)

@app.route("/add", methods=['POST'])
def add():
    title = request.form['title']
    desc = request.form['desc']
    dueby = request.form['dueby']
    trello_items.add_task_trello(title, desc, dueby)
    return redirect(url_for('index'))

@app.route("/done/<id>")
def done(id):
    trello_items.mark_as_done(id)
    return redirect(url_for('index'))

@app.route("/in_progress/<id>")
def in_progress(id):
    trello_items.mark_as_in_progress(id)
    return redirect(url_for('index'))

@app.route("/not_started/<id>")
def not_started(id):
    trello_items.mark_as_not_started(id)
    return redirect(url_for('index'))

@app.route("/delete/<id>")
def delete(id):
    trello_items.delete_task_trello(id)
    return redirect(url_for('index'))

@app.route("/update/<id>")
def show_update_page(id):
    task = trello_items.get_task_trello(id)
    return render_template('update.html', id = id, task = task)
    
@app.route("/update/<id>/submit", methods = ['POST'])
def update_task(id):
    new_title = request.form['title']
    new_desc = request.form['desc']
    new_due = request.form['due']
    trello_items.update_task_trello(id, new_title, new_desc, new_due)
    return index()    
    
@app.route("/sort_status")
def sort_status():
    all_three_lists = [os.getenv("NOTSTARTED_LIST"), os.getenv("INPROGRESS_LIST"), os.getenv("COMPLETED_LIST")]
    tasks = trello_items.sort_by_status(all_three_lists)
    return render_template('index.html', tasks = tasks)

@app.route("/sort_desc")
def sort_desc():
    all_three_lists = [os.getenv("NOTSTARTED_LIST"), os.getenv("INPROGRESS_LIST"), os.getenv("COMPLETED_LIST")]
    tasks = trello_items.sort_by_title(all_three_lists)
    return render_template('index.html', tasks = tasks)

@app.route("/sort_id")
def sort_id():
    all_three_lists = [os.getenv("NOTSTARTED_LIST"), os.getenv("INPROGRESS_LIST"), os.getenv("COMPLETED_LIST")]
    tasks = trello_items.sort_by_id(all_three_lists)
    return render_template('index.html', tasks = tasks)
    
