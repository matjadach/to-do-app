# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install Poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py -UseBasicParsing).Content | python -
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Create Trello Account
Create your Trello account here: https://trello.com/signup

## Obtain your API key and token
Follow the instructions here to generate your API key and token: https://trello.com/app-key

## Add your API key and token to .env file
Add your API key and token in .env file under 'TRELLO'. By convention, environment variable names are all uppercase with underscores e.g. 'API_KEY'

You can also add board ID as well as "Not started", "In progress", "Completed" lists' ids in .env file. They are not sensitive values but it might be a good idea to keep them there as we want it to vary between environments.

## Running the App locally

Once the all dependencies have been installed, start the Flask app in development mode within the Poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Testing the App

To run tests which are kept in todo_app/tests directory use the following:

```bash
$ poetry run pytest or
```

If you wish to run only selected tests:

```bash
$ poetry run pytest todo_app/tests/<the file/test you wish to run>
```

## Running the App on a VM

# VM Provision:
Once on your Control Node, use this command to provision host VM: (You need to know the password to decrypt env_vars.yml)

```bash
$ ansible-playbook Playbook -i Inventory --ask-vault-pass
```

For this command to be successfull you need to make sure you can connect to your Host VM via SSH.

## Running the App in a container (locally)

1. Create a 


To spin up both dev and prod containers use:

```bash
$ docker-compose up
```

If you wish to spin up only one of the containers (either dev or prod):

```bash
$ docker-compose up webapp-prod
```

```bash
$ docker-compose up webapp-dev
```