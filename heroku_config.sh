#!/bin/bash
cd /home/runner/work/to-do-app/to-do-app/
heroku config:set FLASK_APP=todo_app/app -a app-do-to
heroku config:set FLASK_ENV=production -a app-do-to
heroku config:set SECRET_KEY=secret-key -a app-do-to
heroku config:set API_KEY=${{ secrets.API_KEY}} -a app-do-to
heroku config:set API_TOKEN=${{ secrets.API_TOKEN}} -a app-do-to
heroku config:set BOARD=${{ secrets.BOARD}} -a app-do-to
heroku config:set NOTSTARTED_LIST=${{ secrets.NOTSTARTED_LIST}} -a app-do-to
heroku config:set INPROGRESS_LIST=${{ secrets.INPROGRESS_LIST}} -a app-do-to
heroku config:set COMPLETED_LIST=${{ secrets.COMPLETED_LIST}} -a app-do-to