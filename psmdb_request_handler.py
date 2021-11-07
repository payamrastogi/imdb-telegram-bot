# !/usr/bin/env python3

import json

from bson import json_util
from kafka import KafkaConsumer, KafkaProducer

import config_util
from mongodb_client import MongoDBClient

# import logging
# from logging.config import fileConfig
#
# fileConfig('logging.conf')
# logger = logging.getLogger()

RESPONSE_TOPIC = config_util.read_response_topic()
PSMDB_REQUEST_TOPIC = config_util.read_psmdb_request_topic()
BOOTSTRAP_SERVERS = config_util.read_bootstrap_servers()


class PSMDBRequestHandler:
    def __init__(self):
        self.kafka_producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
        self.mongodb_client = MongoDBClient()

    def start(self):
        kafka_consumer = KafkaConsumer(PSMDB_REQUEST_TOPIC,
                                       bootstrap_servers=BOOTSTRAP_SERVERS,
                                       value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        for request in kafka_consumer:
            self.process_request(request)

    def process_request(self, request):
        print(request)
        request = request.value
        request_type = request["type"]
        if request_type == "isseen":
            self.process_is_seen_request(request)
        elif request - type == "search-gte":
            self.process_search_gte_request(request)

    def process_is_seen_request(self, request):
        movie_name = request["query"]
        movies = self.mongodb_client.find_movies_by_name(movie_name)
        print(movies)
        for movie in movies:
            data = self.create_data(movie)
            response = self.create_response(request, data)
            self.publish_response(response)

    def process_search_gte_request(self, request):
        movie_rating = request["query"]
        movies = self.mongodb_client.find_movies_by_rating_gte(movie_rating)
        for movie in movies:
            data = self.create_data(movie)
            response = self.create_response(request, data)
            self.publish_response(response)

    @staticmethod
    def create_data(movie):
        data = {
            "psmdb_id": movie["psmdb_id"],
            "name": movie["name"],
            "psmdb_rating": movie["psmdb_rating"]
        }
        return data

    def publish_response(self, response):
        self.kafka_producer.send(RESPONSE_TOPIC, json.dumps(response, default=json_util.default).encode('utf-8'))
        self.kafka_producer.flush()

    @staticmethod
    def create_response(request, data):
        response = {
            "chat_id": request["chat_id"],
            "type": request["type"],
            "query": request["query"],
            "data": data
        }
        return response


if __name__ == '__main__':
    psmdb_request_handler = PSMDBRequestHandler()
    psmdb_request_handler.start()
