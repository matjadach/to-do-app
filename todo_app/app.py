from flask import Flask, render_template, request, redirect, url_for
from todo_app.data.mongoDB_items import MongoDBTasks
from todo_app.viewmodel import ViewModel
from flask_login import LoginManager, login_required
import os


def create_app():
    app = Flask(__name__)
    mongodb_tasks = MongoDBTasks()

    login_manager = LoginManager()
    
    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(f"https://github.com/login/oauth/authorize?client_id={os.environ.get('CLIENT_ID')}")
    @login_manager.user_loader
    def load_user(user_id):
        pass # We will return to this later
    login_manager.init_app(app)

    @app.route('/')
    @login_required 
    def index():
        tasks = mongodb_tasks.get_all_tasks()
        task_view_model = ViewModel(tasks)
        return render_template('index.html', view_model = task_view_model)

    @app.route("/add", methods=['Post'])
    @login_required 
    def add():
        title = request.form['title']
        desc = request.form['desc']
        dueby = request.form['dueby']
        mongodb_tasks.add_task(title, desc, due=dueby)
        return redirect(url_for('index'))

    @app.route("/done/<id>")
    @login_required 
    def done(id):
        mongodb_tasks.mark_as_done(id)
        return redirect(url_for('index'))

    @app.route("/in_progress/<id>")
    @login_required 
    def in_progress(id):
        mongodb_tasks.mark_as_in_progress(id)
        return redirect(url_for('index'))

    @app.route("/not_started/<id>")
    @login_required 
    def not_started(id):
        mongodb_tasks.mark_as_not_started(id)
        return redirect(url_for('index'))

    @app.route("/delete/<id>")
    @login_required 
    def delete(id):
        mongodb_tasks.delete_task(id)
        return redirect(url_for('index'))

    @app.route("/update/<id>")
    @login_required 
    def show_update_page(id):
        task = mongodb_tasks.get_task(id)
        return render_template('update.html', id = id, task = task)
        
    @app.route("/update/<id>/submit", methods = ['POST'])
    @login_required 
    def update_task(id):
        new_title = request.form['title']
        new_desc = request.form['desc']
        new_due = request.form['due']
        mongodb_tasks.update_task(id, new_title, new_desc, new_due)
        return index()

    @app.route('/index_with_all_completed')
    @login_required 
    def index_with_all_completed():
        tasks = mongodb_tasks.get_all_tasks()
        task_view_model = ViewModel(tasks)
        return render_template('index_with_all_completed.html', view_model = task_view_model)

    return app

if __name__ == '__main__':
    create_app().run()