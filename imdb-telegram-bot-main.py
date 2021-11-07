# !/usr/bin/env python3
from telegram_request_handler import TelegramRequestHandler
from general_request_handler import GeneralRequestHandler
from imdb_request_handler import IMDBRequestHandler
from psmdb_request_handler import PSMDBRequestHandler

import logging
from logging.config import fileConfig

fileConfig('logging.conf')
logger = logging.getLogger()


class IMDBTelegramBotMain:
    def __init__(self):
        self.telegram_request_handler = TelegramRequestHandler()
        self.general_request_handler = GeneralRequestHandler()
        self.imdb_request_handler = IMDBRequestHandler()
        self.psmdb_request_handler = PSMDBRequestHandler()


if __name__ == '__main__':
    imdb_telegram_bot = IMDBTelegramBotMain()
