# !/usr/bin/env python3

import json
from kafka import KafkaConsumer

import config_util
from mongodb_client import MongoDBClient


class RecommendationRequestHandler:
    def __init__(self):
        # self.kafka_producer = KafkaProducer(bootstrap_servers=config_util.read_bootstrap_servers())
        self.mongodb_client = MongoDBClient()

    def start(self):
        kafka_consumer = KafkaConsumer(config_util.read_recommendation_topic(),
                                       bootstrap_servers=config_util.read_bootstrap_servers(),
                                       value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        for request in kafka_consumer:
            self.process_request(request)

    def process_request(self, request):
        print(request)
        request = request.value
        request_type = request["type"]
        if request_type == "add":
            self.process_add_request(request)

    def process_add_request(self, request):
        movie = request["data"]
        print(movie)
        self.mongodb_client.insert_movie_recommendation(movie)


if __name__ == '__main__':
    recommendation_request_handler = RecommendationRequestHandler()
    recommendation_request_handler.start()
