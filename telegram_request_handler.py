# !/usr/bin/env python3
import datetime  # Importing the datetime library
import json
from time import sleep  # Importing the time library to provide the delays in program

import telepot  # Importing the telepot library
from bson import json_util
from kafka import KafkaProducer
from telepot.loop import MessageLoop  # Library function to communicate with telegram bot

from config_util import read_telegram_bot_token


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
        chat_id = msg['chat']['id']  # Receiving the message from telegram
        command = msg['text']  # Getting text from the message

        print("Received:", command)

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

    def process_search_command(self, chat_id, command):
        search = command.split("/search", 1)
        if search and len(search) == 2:
            request = {
                "command": "search",
                "query": search[1].lstrip(),
                "chat_id": chat_id
            }
            self.kafka_producer.send("imdb_request_topic",
                                     json.dumps(request, default=json_util.default).encode('utf-8'))

    def process_date_command(self, chat_id):
        now = datetime.datetime.now()
        self.bot.sendMessage(chat_id,
                             str("Date: ") + str(now.day) + str("/") + str(now.month) + str("/") + str(now.year))

    def process_time_command(self, chat_id):
        now = datetime.datetime.now()
        self.bot.sendMessage(chat_id,
                             str("Time: ") + str(now.hour) + str(":") + str(now.minute) + str(":")
                             + str(now.second))

    def process_help_command(self, chat_id):
        self.bot.sendMessage(chat_id, str("[/search <movie_name>] returns rating, year, and genres"))

    def publish_request(self, request, topic):
        self.kafka_producer.send(topic,
                                 json.dumps(request, default=json_util.default).encode('utf-8'))

    @staticmethod
    def create_create_request(chat_id, query):
        request = {
            "type": "search",
            "query": query,
            "chat_id": chat_id
        }
        return request
