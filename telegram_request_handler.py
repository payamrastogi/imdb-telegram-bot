# !/usr/bin/env python3
import json
import logging
from logging.config import fileConfig
from time import sleep  # Importing the time library to provide the delays in program

import telepot  # Importing the telepot library
from bson import json_util
from kafka import KafkaProducer
from telepot.loop import MessageLoop  # Library function to communicate with telegram bot

from config_util import read_telegram_bot_token

fileConfig('logging.conf')
logger = logging.getLogger()


class TelegramRequestHandler:
    def __init__(self):
        self.bot = telepot.Bot(read_telegram_bot_token())
        print(self.bot.getMe())
        self.kafka_producer = KafkaProducer(bootstrap_servers='192.168.1.23:9092')
        self.start()

    # Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
    def start(self):
        MessageLoop(self.bot, self.handle).run_as_thread()
        print('Listening....')
        while 1:
            sleep(10)

    def handle(self, msg):
        logger.info('handle: start', msg)
        chat_id = msg['chat']['id']  # Receiving the message from telegram
        command = msg['text']  # Getting text from the message
        print(command)
        # Comparing the incoming message to send a reply according to it
        if command == '/hi':
            self.bot.sendMessage(chat_id, str("Hi! from crunch"))
        elif command == '/help':
            self.process_help_command(chat_id)
        elif command == '/time':
            self.process_time_command(chat_id)
        elif command == '/date':
            self.process_date_command(chat_id)
        elif '/search' in command:
            self.process_search_command(chat_id, command)
        elif '/isseen' in command:
            self.process_isseen_command(chat_id, command)

    def process_isseen_command(self, chat_id, command):
        logger.info('process_isseen_command: start')
        isseen = command.split("/isseen", 1)
        if isseen and len(isseen) == 2:
            request = {
                "type": "isseen",
                "query": isseen[1].strip(),
                "chat_id": chat_id
            }
            self.publish_request("psmdb_request_topic", request)

    def process_search_command(self, chat_id, command):
        logger.info('process_search_command: start')
        search = command.split("/search", 1)
        if search and len(search) == 2:
            request = {
                "type": "search",
                "query": search[1].strip(),
                "chat_id": chat_id
            }
            self.publish_request("imdb_request_topic", request)

    def process_date_command(self, chat_id):
        logger.info('process_date_command: start')
        request = {
            "type": "date",
            "query": None,
            "chat_id": chat_id
        }
        self.publish_request("general_request_topic", request)

    def process_time_command(self, chat_id):
        logger.info('process_time_command: start')
        request = {
            "type": "time",
            "query": None,
            "chat_id": chat_id
        }
        self.publish_request("general_request_topic", request)

    def process_help_command(self, chat_id):
        logger.info('process_help_command: start')
        request = {
            "type": "help",
            "query": None,
            "chat_id": chat_id
        }
        self.publish_request("general_request_topic", request)

    def publish_request(self, topic, request):
        logger.info('publish_request: start')
        if topic and request:
            self.kafka_producer.send(topic, json.dumps(request, default=json_util.default).encode('utf-8'))
            self.kafka_producer.flush()

