#!/bin/bash
poetry run gunicorn -b 0.0.0.0:$PORT -w 2 app_run:app