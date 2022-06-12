#!/bin/bash
cd /home/runner/work/to-do-app/to-do-app/
touch .env
echo "FLASK_APP=todo_app/app" >> .env
echo "FLASK_.env=production" >> .env
echo "SECRET_KEY=secret-key" >> .env
echo "API_KEY=$API_KEY" >> .env
echo "API_TOKEN=$API_TOKEN" >> .env
echo "BOARD=$BOARD" >> .env
echo "NOTSTARTED_LIST=$NOTSTARTED_LIST" >> .env
echo "INPROGRESS_LIST=$INPROGRESS_LIST" >> .env
echo "COMPLETED_LIST=$COMPLETED_LIST" >> .env