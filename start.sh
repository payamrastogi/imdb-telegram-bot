#!/bin/bash

mkdir log
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
nohup python telegram_request_handler.py &
nohup python general_request_handler.py &
nohup python imdb_request_handler.py &
nohup python psmdb_request_handler.py &
nohup python response_handler.py &