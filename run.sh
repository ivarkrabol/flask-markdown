#!/bin/bash

source ~/.virtualenvs/flask-markdown/bin/activate
FLASK_APP=flaskmarkdown FLASK_DEBUG=TRUE flask run
