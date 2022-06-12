#!/bin/bash
cd /home/runner/work/to-do-app/to-do-app/
heroku config:set `cat .env | grep FLASK_APP` -a app-do-to
heroku config:set `cat .env | grep FLASK_ENV` -a app-do-to
heroku config:set `cat .env | grep SECRET_KEY` -a app-do-to
heroku config:set `cat .env | grep API_KEY` -a app-do-to
heroku config:set `cat .env | grep API_TOKEN` -a app-do-to
heroku config:set `cat .env | grep BOARD` -a app-do-to
heroku config:set `cat .env | grep NOTSTARTED_LIST` -a app-do-to
heroku config:set `cat .env | grep INPROGRESS_LIST` -a app-do-to
heroku config:set `cat .env | grep COMPLETED_LIST` -a app-do-to