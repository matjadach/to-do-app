#!/bin/bash
cd /home/runner/work/to-do-app/to-do-app/
touch .env.testing
echo "FLASK_APP=todo_app/app" >> .env.testing
echo "FLASK_ENV=production" >> .env.testing
echo "SECRET_KEY=secret-key" >> .env.testing
echo $API_KEY >> .env.testing
echo $API_TOKEN >> .env.testing
echo $BOARD >> .env.testing
echo $NOTSTARTED_LIST >> .env.testing
echo $INPROGRESS_LIST >> .env.testing
echo $COMPLETED_LIST >> .env.testing