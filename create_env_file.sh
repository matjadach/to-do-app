#!/bin/bash
cd /home/runner/work/to-do-app/to-do-app/
touch .envtest
echo "FLASK_APP=todo_app/app" >> .envtest
echo "FLASK_envtest=production" >> .envtest
echo "SECRET_KEY=secret-key" >> .envtest
echo "API_KEY=$API_KEY" >> .envtest
echo "API_TOKEN=$API_TOKEN" >> .envtest
echo "BOARD=$BOARD" >> .envtest
echo "NOTSTARTED_LIST=$NOTSTARTED_LIST" >> .envtest
echo "INPROGRESS_LIST=$INPROGRESS_LIST" >> .envtest
echo "COMPLETED_LIST=$COMPLETED_LIST" >> .envtest