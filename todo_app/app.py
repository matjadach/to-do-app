from flask import Flask, render_template, request, redirect, url_for
from todo_app.data.mongoDB_items import MongoDBTasks
from todo_app.viewmodel import ViewModel
from flask_login import LoginManager


def create_app():
    app = Flask(__name__)
    mongodb_tasks = MongoDBTasks()

    login_manager = LoginManager()
    
    @login_manager.unauthorized_handler
    def unauthenticated():
        pass # Add logic to redirect to the GitHub OAuth flow when unauthenticated
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
    def add():
        title = request.form['title']
        desc = request.form['desc']
        dueby = request.form['dueby']
        mongodb_tasks.add_task(title, desc, due=dueby)
        return redirect(url_for('index'))

    @app.route("/done/<id>")
    def done(id):
        mongodb_tasks.mark_as_done(id)
        return redirect(url_for('index'))

    @app.route("/in_progress/<id>")
    def in_progress(id):
        mongodb_tasks.mark_as_in_progress(id)
        return redirect(url_for('index'))

    @app.route("/not_started/<id>")
    def not_started(id):
        mongodb_tasks.mark_as_not_started(id)
        return redirect(url_for('index'))

    @app.route("/delete/<id>")
    def delete(id):
        mongodb_tasks.delete_task(id)
        return redirect(url_for('index'))

    @app.route("/update/<id>")
    def show_update_page(id):
        task = mongodb_tasks.get_task(id)
        return render_template('update.html', id = id, task = task)
        
    @app.route("/update/<id>/submit", methods = ['POST'])
    def update_task(id):
        new_title = request.form['title']
        new_desc = request.form['desc']
        new_due = request.form['due']
        mongodb_tasks.update_task(id, new_title, new_desc, new_due)
        return index()

    @app.route('/index_with_all_completed')
    def index_with_all_completed():
        tasks = mongodb_tasks.get_all_tasks()
        task_view_model = ViewModel(tasks)
        return render_template('index_with_all_completed.html', view_model = task_view_model)

    return app

if __name__ == '__main__':
    create_app().run()