#!/bin/bash
cd /home/runner/work/to-do-app/to-do-app/
touch .env
echo "FLASK_APP=todo_app/app" >> .env
echo "FLASK_.env=production" >> .env
echo "SECRET_KEY=secret-key" >> .env
echo "API_KEY=${{ secrets.API_KEY}}" >> .env
echo "API_TOKEN=${{ secrets.API_TOKEN}}" >> .env
echo "BOARD=${{ secrets.BOARD}}" >> .env
echo "NOTSTARTED_LIST=${{ secrets.NOTSTARTED_LIST}}" >> .env
echo "INPROGRESS_LIST=${{ secrets.INPROGRESS_LIST}}" >> .env
echo "COMPLETED_LIST=${{ secrets.COMPLETED_LIST}}" >> .env

