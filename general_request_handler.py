# !/usr/bin/env python3
import datetime  # Importing the datetime library
import json

from bson import json_util
from kafka import KafkaConsumer, KafkaProducer

import config_util

RESPONSE_TOPIC = config_util.read_response_topic()
GENERAL_REQUEST_TOPIC = config_util.read_general_request_topic()
BOOTSTRAP_SERVERS = config_util.read_bootstrap_servers()


class GeneralRequestHandler:
    def __init__(self):
        self.kafka_consumer = KafkaConsumer(GENERAL_REQUEST_TOPIC, bootstrap_servers=BOOTSTRAP_SERVERS)
        self.kafka_producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
        for request in self.kafka_consumer:
            self.process_request(request)

    def process_request(self, request):
        request = json.load(request)
        request_type = request["type"]
        request_chat_id = request["chat_id"]
        if request_type == "date":
            self.process_date_command(request_chat_id, request_type)
        elif request_type == "time":
            self.process_time_command(request_chat_id, request_type)
        elif request_type == "help":
            self.process_help_command(request_chat_id, request_type)

    def process_date_command(self, chat_id, request_type):
        now = datetime.datetime.now()
        data = str("Date: ") + str(now.day) + str("/") + str(now.month) + str("/") + str(now.year)
        response = self.create_response(chat_id, request_type, data)
        self.publish_response(response)

    def process_time_command(self, chat_id, request_type):
        now = datetime.datetime.now()
        data = str("Time: ") + str(now.hour) + str(":") + str(now.minute) + str(":") + str(now.second)
        response = self.create_response(chat_id, request_type, data)
        self.publish_response(response)

    def process_help_command(self, chat_id, request_type):
        data = str("[/search <movie_name>] returns rating, year, and genres from IMDB")
        response = self.create_response(chat_id, request_type, data)
        self.publish_response(response)

    def publish_response(self, response):
        self.kafka_producer.send(RESPONSE_TOPIC, json.dumps(response, default=json_util.default).encode('utf-8'))
        self.kafka_producer.flush()

    @staticmethod
    def create_response(chat_id, request_type, data):
        response = {
            "chat_id": chat_id,
            "type": request_type,
            "data": data
        }
        return response


if __name__ == '__main__':
    generalRequestHandler = GeneralRequestHandler()