from flask import Flask, render_template, request, redirect, url_for
from todo_app.flask_config import Config
from todo_app.data import trello_items
from todo_app.viewmodel import ViewModel
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config())
    trello_items.load_config()

    @app.route('/')
    def index():
        all_three_lists = [os.getenv("NOTSTARTED_LIST"), os.getenv("INPROGRESS_LIST"), os.getenv("COMPLETED_LIST")]
        tasks = trello_items.get_tasks_trello(all_three_lists)
        task_view_model = ViewModel(tasks)
        return render_template('index.html', view_model = task_view_model)

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

    @app.route('/index_with_all_completed')
    def index_with_all_completed():
        all_three_lists = [os.getenv("NOTSTARTED_LIST"), os.getenv("INPROGRESS_LIST"), os.getenv("COMPLETED_LIST")]
        tasks = trello_items.get_tasks_trello(all_three_lists)
        task_view_model = ViewModel(tasks)
        return render_template('index_with_all_completed.html', view_model = task_view_model)

    return app