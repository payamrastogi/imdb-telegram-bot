#!/bin/bash

mkdir log
virtualenv .venv
source .venv/bin/activate
pip install -r requirements.txt
nohup python telegram_request_handler.py &
echo $! >> imdb-telegram-bot.pid
nohup python general_request_handler.py &
echo $! >> imdb-telegram-bot.pid
nohup python imdb_request_handler.py &
echo $! >> imdb-telegram-bot.pid
nohup python psmdb_request_handler.py &
echo $! >> imdb-telegram-bot.pid
nohup python recommendation_request_handler.py &
echo $! >> imdb-telegram-bot.pid
nohup python response_handler.py &
echo $! >> imdb-telegram-bot.pid