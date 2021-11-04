import json

from bson import json_util
from imdb import IMDb, IMDbError
from kafka import KafkaConsumer, KafkaProducer

import config_util

RESPONSE_TOPIC = config_util.read_response_topic()
IMDB_REQUEST_TOPIC = config_util.read_imdb_request_topic()
BOOTSTRAP_SERVERS = config_util.read_bootstrap_servers()


class IMDBRequestHandler:
    def __init__(self):
        self.kafka_consumer = KafkaConsumer(IMDB_REQUEST_TOPIC, bootstrap_servers=BOOTSTRAP_SERVERS)
        self.kafka_producer = KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS)
        self.imdb_client = IMDb()
        for request in self.kafka_consumer:
            self.process_request(request)

    def process_request(self, request):
        request = json.load(request)
        request_type = request["type"]
        if request_type == "search":
            self.find_movies(request)
        elif request_type == "search_with_plot":
            self.find_movie(request, True)

    def find_movies(self, request, with_plot=False):
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
        data = {
            "imdb_id": movie_id,
            "name": movie.data['title'],
            "year": movie.data['year'],
            "imdb_rating": movie.data['rating'],
            "genres": movie.data['genres']
        }
        if with_plot:
            movie.infoset2keys
            data["plot"] = movie.get('plot')
        return data

    def publish_response(self, response):
        self.kafka_producer.send(RESPONSE_TOPIC, json.dumps(response, default=json_util.default).encode('utf-8'))
        self.kafka_producer.flush()
