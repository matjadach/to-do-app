#!/bin/bash
cd /home/runner/work/to-do-app/to-do-app/
touch .env
echo "FLASK_APP=todo_app/app" >> .env
echo "FLASK_ENV=production" >> .env
echo "SECRET_KEY=secret-key" >> .env
echo $API_KEY >> .env
echo $API_TOKEN >> .env
echo $BOARD >> .env
echo $NOTSTARTED_LIST >> .env
echo $INPROGRESS_LIST >> .env
echo $COMPLETED_LIST >> .env