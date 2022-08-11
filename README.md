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

To spin up all three containers(dev, test & prod) use the following command:

```bash
$ docker-compose up
```

If you wish to spin up only one of the containers (either dev, test or prod) use respecitively either (Note: if you wish to run the prod container locally please change "$PORT" in gunicorn.sh to "80"):

```bash
$ docker-compose up webapp-prod
```

```bash
$ docker-compose up webapp-dev
```

```bash
$ docker-compose up webapp-test
```

## Deploying the App on Azure

To deploy the app on Azure follow the below steps:

1. Log in to Azure (You need to set up an account first - go to https://signup.azure.com/ to sign up )

```bash
$ az login
```

2. Create an App Service Plan 

```bash
$ az appservice plan create -g {Your resource group name eg. test-resource-group-01} -n {Name of the service app plan you wish to create e.g. test-asp-01 } --sku {e.g. B1} --is-Linux
```


3. Create a Web App and deploy the production image container

```bash
$ az webapp create -g {Your resource group name} --plan {Your app service plan name} --name {Name of your app. Needs to be unique globally e.g. test-app-01} --deployment-container-image-name {docker hub username/name of the image and a tag e.g. username/your_apps_image:latest}
```

4. Configure your app

First, create a file called "env.json" in which set all the environment variables following the format below:

```bash
{
  "CONFIG_KEY_01": "CONFIG_VALUE_01",
  "CONFIG_KEY_02": "CONFIG_VALUE_02"
}
```

Then run the following command:

```bash
$ az webapp config appsettings set -g {Your resource group name eg. test-resource-group-01} -n {Name of your app} --settings @env.json
```

5. Confirm your app is up and running

Go to http://{Your web app name}.azurewebsites.net/

## Using MongoDB for tasks storage.

1. Log into Azure and create MongoDB cluster either via the Portal UI or with the CLI.

### With the Portal:
• New → CosmosDB Database
• Select "Azure Cosmos DB API for MongoDB"
• Choose "Serverless" for Capacity mode
• Create new collection within your databse.
• You can also configure secure firewall connections here, but for now you should permit access from "All Networks" to enable easier testing of the integration with the app.
### With the CLI:
• Create new CosmosDB Account by typing in your terminal:
`az cosmosdb create --name <cosmos_account_name> --resource-group <resource_group_name> --kind MongoDB --capabilities EnableServerless -- server-version 3.6`
• Create new MongoDB database under that account:
`az cosmosdb mongodb database create --account-name <cosmos_account_name> --name <database_name> --resource-group <resource_group_name>`
• Create new collection under that database account:
`az cosmosdb mongodb collection create --account-name <cosmos_account_name> --databasename <database_name>  --name <collection_name>  --resource-group <resource_group_name>`

Obtain "Primary Connection String" to connect to your MongoDB instance. You can find it under "Settings" in the Azure Portal UI.

1. Repeat Step 4 from 'Deploying the App on Azure' paragraph, but first populate your .envjson with the following:
```bash
{
  "DB_CONNECTION_STRING": "<Primary Connection String>",
  "TASKS_DB_NAME": "<database_name>",
  "COLLECTION_NAME": "<collection_name>"
}
```
Remember to rerun the azure cli command from Step 4.

3. Task transfer from Trello to MongoDB

To transfer tasks from Trello to MongoDB instance, run `python3 migrate.py` in the root folder of this repo. By default it will delete the tasks from Trello during the migration. If you wish to change this behaviour set 'delete_after_transfer' value in 'migrate.py' file to False.

4. Confirm your app is and running. Check if all your tasks from Trello have been migrated.

Go to "http://{Your web app name}.azurewebsites.net/"