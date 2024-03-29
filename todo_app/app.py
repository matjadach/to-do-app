from flask import Flask, render_template, request, redirect, url_for
from todo_app.data.mongoDB_items import MongoDBTasks
from todo_app.viewmodel import ViewModel
from todo_app.user import User
from todo_app.flask_config import Config
from flask_login import LoginManager, login_required, login_user, current_user
import os, requests, logging
from functools import wraps
from loggly.handlers import HTTPSHandler
from pythonjsonlogger import jsonlogger


def create_app():
    app = Flask(__name__)
    mongodb_tasks = MongoDBTasks()
    app.config.from_object(Config())
    login_manager = LoginManager()

    #Logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    text_formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    console_handler.setFormatter(text_formatter)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(app.config['LOG_LEVEL'])
    if app.config['LOGGLY_TOKEN'] is not None:
        https_handler = HTTPSHandler(f"https://logs-01.loggly.com/inputs/{app.config['LOGGLY_TOKEN']}/tag/todo-app")
        json_formatter = jsonlogger.JsonFormatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
        https_handler.setFormatter(json_formatter)
        app.logger.addHandler(https_handler)
    
    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(f"https://github.com/login/oauth/authorize?client_id={os.environ.get('CLIENT_ID')}")
    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)
    login_manager.init_app(app)

    @app.route('/login/callback', methods=['GET'])
    def login_callback():

        # Use Flask's 'request' method to get 'code'
        code = request.args.get('code')

        # Step 1. Obtain access token by piping in 'code' from redirect
        access_token_url = "https://github.com/login/oauth/access_token"
        access_token_params = { 
            "client_id": os.environ.get('CLIENT_ID'),
            "client_secret": os.environ.get('CLIENT_SECRET'),
            "code": code 
            }
        access_token_headers = {
            "Accept": "application/json"
            }
        response = requests.post(access_token_url, params=access_token_params, headers=access_token_headers).json()
        if response.status_code != 200:
            app.logger.error("There was an issue when obtaining OAuth access token.")
        access_token = (requests.post(access_token_url, params=access_token_params, headers=access_token_headers)).json()["access_token"]

        # Step 2. Use access token to call user info endpoint and obtain 'id'
        user_info_url = "https://api.github.com/user"
        user_info_headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {access_token}"
        }
        id = (requests.get(user_info_url, headers=user_info_headers)).json()['id']

        # Step 3. Create an instance of User using 'id' from Step 2 and login that user.
        user = User(user_id=id)
        app.logger.info(f"User with ID: {user.user_id} is now logged in.")
        login_user(user)
        return redirect(url_for('index'))

    def authorise_user(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            if current_user.role == 'admin':
                logger.info("Succssfully authorised as admin user.")
                return f(*args, **kwargs)
            else:
                logger.warning("The current user does not have the permissions to view this page.")
                return render_template('unauthorised.html'), 403
        return decorator


    @app.route('/')
    @login_required
    def index():
        tasks = mongodb_tasks.get_all_tasks()
        task_view_model = ViewModel(tasks)
        if current_user.is_anonymous or current_user.role == 'admin':
            return render_template('index.html', view_model = task_view_model)
        else:
            return render_template('index_with_hidden_buttons.html', view_model = task_view_model)

    @app.route("/add", methods=['Post'])
    @login_required 
    @authorise_user
    def add():
        title = request.form['title']
        desc = request.form['desc']
        dueby = request.form['dueby']
        mongodb_tasks.add_task(title, desc, due=dueby)
        app.logger.info(f"Task: '{title}' has been added.")
        return redirect(url_for('index'))


    @app.route("/done/<id>")
    @login_required 
    @authorise_user
    def done(id):
        mongodb_tasks.mark_as_done(id)
        app.logger.info(f"Task with ID: {id} has been marked as 'done' by the user with ID: {current_user.user_id}.")
        return redirect(url_for('index'))


    @app.route("/in_progress/<id>")
    @login_required 
    @authorise_user
    def in_progress(id):
        mongodb_tasks.mark_as_in_progress(id)
        app.logger.info(f"Task with ID: {id} has been marked as 'in progress' by the user with ID: {current_user.user_id}.")
        return redirect(url_for('index'))

    @app.route("/not_started/<id>")
    @login_required
    @authorise_user
    def not_started(id):
        mongodb_tasks.mark_as_not_started(id)
        app.logger.info(f"Task with ID: {id} has been marked as 'not started' by the user with ID: {current_user.user_id}.")
        return redirect(url_for('index'))

    @app.route("/delete/<id>")
    @login_required 
    @authorise_user
    def delete(id):
        mongodb_tasks.delete_task(id)
        app.logger.info(f"Task with ID: {id} has been deleted by the user with ID: {current_user.user_id}.")
        return redirect(url_for('index'))


    @app.route("/update/<id>")
    @login_required
    @authorise_user
    def show_update_page(id):
        task = mongodb_tasks.get_task(id)
        return render_template('update.html', id = id, task = task)
        
    @app.route("/update/<id>/submit", methods = ['POST'])
    @login_required
    @authorise_user
    def update_task(id):
        new_title = request.form['title']
        new_desc = request.form['desc']
        new_due = request.form['due']
        mongodb_tasks.update_task(id, new_title, new_desc, new_due)
        app.logger.info(f"Task with ID: {id} has been updated. Its new title is: '{new_title}', new description: '{new_desc}' and it is now due by '{new_due}'. This task has been updated by the user with ID: {current_user.user_id}.")
        return index()


    @app.route('/index_with_all_completed')
    @login_required
    def index_with_all_completed():
        tasks = mongodb_tasks.get_all_tasks()
        task_view_model = ViewModel(tasks)
        if current_user.role == 'admin':
            return render_template('index_with_all_completed.html', view_model = task_view_model)
        else:
            return render_template('index_with_all_completed_with_hidden_buttons.html', view_model = task_view_model)

    return app

if __name__ == '__main__':
    create_app().run()