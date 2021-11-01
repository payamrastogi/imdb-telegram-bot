import pymongo


class MongoDBClient:
    def __init__(self):
        try:
            mongo_uri = "mongodb://192.168.1.23:27017"
            self.mongo_client = pymongo.MongoClient(mongo_uri)
            self.movie_db = self.mongo_client["moviedb"]
        except Exception as e:
            print("could not connect to MongoDB", e)

    def insert_movie(self, movie):
        if movie:
            movies_collection = self.movie_db.movies
            movies_collection.insert_one(movie)

    def insert_series(self, series):
        if series:
            series_collection = self.movie_db.series
            series_collection.insert_one(series)

if __name__ == '__main__':
    mongo = MongoDBClient()
    movie = {'movie_name': 'the witcher: nightmare of the wolf', 'movie_rating': '3.5'}
    mongo.insert_movie(movie)
