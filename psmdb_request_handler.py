# !/usr/bin/env python3

import json
import re
from bson import json_util
from kafka import KafkaConsumer, KafkaProducer

import config_util
from mongodb_client import MongoDBClient

# import logging
# from logging.config import fileConfig
#
# fileConfig('logging.conf')
# logger = logging.getLogger()


class PSMDBRequestHandler:
    def __init__(self):
        self.kafka_producer = KafkaProducer(bootstrap_servers=config_util.read_bootstrap_servers()) # comment this if you want to insert manually
        self.mongodb_client = MongoDBClient()

    def start(self):
        kafka_consumer = KafkaConsumer(config_util.read_psmdb_request_topic(),
                                       bootstrap_servers=config_util.read_bootstrap_servers(),
                                       value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        for request in kafka_consumer:
            self.process_request(request)

    def process_file(self, filename):
        count_movies = 0
        count_series = 0
        with open(filename) as file:
            for line in file:
                line = line.strip().lower()
                if self.is_series(line):
                    series = self.get_series_details(line)
                    # print(series)
                    res = self.mongodb_client.insert_or_update_series(series)
                    if res:
                        count_series = count_series + 1
                else:
                    movie = self.get_movie_details(line)
                    res = self.mongodb_client.insert_movie(movie)
                    if res:
                        count_movies = count_movies + 1
        print(count_series)
        print(count_movies)
        print(count_series + count_movies)

    def process_request(self, request):
        print(request)
        request = request.value
        request_type = request["type"]
        if request_type == "isseen":
            self.process_is_seen_request(request)
        elif request_type == "search-gte":
            self.process_search_gte_request(request)
        elif request_type == "watched":
            self.process_watched_request(request)

    def process_is_seen_request(self, request):
        movie_name = request["query"]
        movies = self.mongodb_client.find_movies_by_name(movie_name)
        self.process_movie_list(request, movies)

    def process_search_gte_request(self, request):
        movie_rating = request["query"]
        movies = self.mongodb_client.find_movies_by_rating_gte(movie_rating)
        self.process_movie_list(request, movies)

    def process_watched_request(self, request):
        query = request["query"]
        print(query)
        if self.is_series(query):
            print("is series")
            series = self.get_series_details(query)
            print(series)
            res = self.mongodb_client.insert_or_update_series(series)
        else:
            print("is movie")
            movie = self.get_movie_details(query)
            res = self.mongodb_client.insert_movie(movie)
        if res:
            data = self.create_status_data("success")
        else:
            data = self.create_status_data("failed")
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

    def process_movie_list(self, request, movies):
        print(movies)
        if movies:
            for movie in movies:
                data = self.create_data(movie)
                response = self.create_response(request, data)
                self.publish_response(response)
        else:
            data = self.create_empty_data()
            response = self.create_response(request, data)
            self.publish_response(response)

    def publish_response(self, response):
        self.kafka_producer.send(config_util.read_response_topic(), json.dumps(response, default=json_util.default).encode('utf-8'))
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

    @staticmethod
    def create_empty_data():
        data = {
            "result": "No movie found"
        }
        return data

    @staticmethod
    def create_status_data(status):
        data = {
            "status": status
        }
        return data

    @staticmethod
    def is_series(text):
        if text and text.lower().startswith("series:"):
            return True
        else:
            return False

    def get_series_details(self, text):
        text = text.strip().lower()
        series_name = self.get_series_name(text)
        series_season_number = self.get_series_season_number(text)
        series_rating = self.get_series_rating(text)
        return {'series_name': series_name, 'series_season_number': series_season_number,
                'series_rating': series_rating}

    @staticmethod
    def get_series_name(text):
        text = text.strip().lower()
        series_name = re.search('series:[0-9 ]*([a-z0-9:.%,&\\- ]*)season:[0-9 ]*[0-9.() ]*', text)
        if series_name:
            return series_name.group(1).strip()
        else:
            return None

    @staticmethod
    def get_series_rating(text):
        text = text.strip().lower()
        series_rating = re.search('series:[0-9 ]*[a-z0-9:.%,&\\- ]*season:[0-9 ]*[(]*([0-9.]*)[)]*', text)
        if series_rating:
            return series_rating.group(1)
        else:
            return None

    @staticmethod
    def get_series_season_number(text):
        text = text.strip().lower()
        series_season_number = re.search('series:[0-9 ]*[a-z0-9:.%,&\\- ]*season:([0-9 ]*)[0-9.() ]*', text)
        if series_season_number:
            return series_season_number.group(1)
        else:
            return None

    def get_movie_details(self, text):
        text = text.strip().lower()
        movie_name = self.get_movie_name(text)
        movie_rating = self.get_movie_rating(text)
        return {'movie_name': movie_name, 'movie_rating': movie_rating}

    @staticmethod
    def get_movie_name(text):
        text = text.strip().lower()
        movie_name = re.search('([a-z0-9:.%,&\\- ]*)[(]?[0-9.]*[)]?', text)
        if movie_name:
            return movie_name.group(1).strip()
        else:
            return None

    @staticmethod
    def get_movie_rating(text):
        text = text.strip().lower()
        movie_rating = re.search('[a-z0-9:.%,&\\- ]*[(]?([0-9.]*)[ )]?', text)
        if movie_rating:
            return movie_rating.group(1)
        else:
            return None


if __name__ == '__main__':
    psmdb_request_handler = PSMDBRequestHandler()
    psmdb_request_handler.start() # comment this if you want to insert manually
    #psmdb_request_handler.process_file('movies.txt') # uncomment this if you want to insert manually
