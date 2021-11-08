# !/usr/bin/env python3

import json
import copy
from bson import json_util
from imdb import IMDb, IMDbError
from kafka import KafkaConsumer, KafkaProducer

import config_util

# import logging
# from logging.config import fileConfig
# fileConfig('logging.conf')
# logger = logging.getLogger()


class IMDBRequestHandler:
    def __init__(self):
        self.kafka_producer = KafkaProducer(bootstrap_servers=config_util.read_bootstrap_servers())
        self.imdb_client = IMDb()

    def start(self):
        kafka_consumer = KafkaConsumer(config_util.read_imdb_request_topic(),
                                       bootstrap_servers=config_util.read_bootstrap_servers(),
                                       value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        for request in kafka_consumer:
            self.process_request(request)

    def process_request(self, request):
        #logger.info('process_request: start request:{}', request)
        request = request.value
        request_type = request["type"]
        if request_type == "search":
            self.find_movies(request)
        elif request_type == "search_with_plot":
            self.find_movies(request, True)

    def find_movies(self, request, with_plot=False):
        #logger.info('find_movies: start request:{}', request)
        query = request["query"]
        if query:
            try:
                movies = self.imdb_client.search_movie(query)
                for movie in movies:
                    try:
                        movie_detail = self.imdb_client.get_movie(movie.movieID)
                        data = self.create_data(movie.movieID, movie_detail, with_plot)
                        response = self.create_response(request, data)
                        self.publish_response(response)
                    except (IMDbError, KeyError) as err:
                        print(err)
            except IMDbError as e:
                print(e)

    @staticmethod
    def create_response(request, data):
        response = {
            "chat_id": request["chat_id"],
            "type": request["type"],
            "query": request["query"],
            "data": data
        }

        return response

    @staticmethod
    def create_data(movie_id, movie, with_plot):
        data = {"imdb_id": movie_id, "name": movie.data['title']}
        if "rating" in movie.data:
            data["imdb_rating"] = movie.data['rating']
        if "year" in movie.data:
            data["year"] = movie.data['year']
        if "genres" in movie.data:
            data["genres"] = movie.data['genres']
        if with_plot:
            movie.infoset2keys
            if "plot" in movie:
                data["plot"] = movie.get('plot')
        return data

    def publish_response(self, response):
        if response and response["type"] == "search":
            res = copy.deepcopy(response)
            res["type"] = "add"
            self.kafka_producer.send(config_util.read_recommendation_topic(), json.dumps(res, default=json_util.default).encode('utf-8'))
            self.kafka_producer.flush()
        self.kafka_producer.send(config_util.read_response_topic(), json.dumps(response, default=json_util.default).encode('utf-8'))
        self.kafka_producer.flush()


if __name__ == '__main__':
    imdb_request_handler = IMDBRequestHandler()
    imdb_request_handler.start()
