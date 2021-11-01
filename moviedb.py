import pymongo
from bson import ObjectId


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
            mov = {'name': movie['movie_name'], 'rating': movie['movie_rating']}
            movies_collection.insert_one(mov)
            return True
        return False

    def find_movies_by_name(self, movie_name):
        movies = []
        if movie_name:
            movies_collection = self.movie_db.movies
            res = movies_collection.find({'name': {'$regex': movie_name.strip().lower(),  '$options': 'i'}})
            for movie in res:
                movies.append({"name": movie["name"], "ps_rating": movie["rating"]})
            return movies
        return []

    def find_movie_by_id(self, movie_id):
        if movie_id:
            movies_collection = self.movie_db.movies
            movie = movies_collection.find_one({"_id": ObjectId(movie_id)})
            return movie
        return None

    def insert_or_update_series(self, series):
        if series:
            s = self.find_series_by_name(series['series_name'])
            print(s)
            if s:
                return self.update_series(series, s)
            else:
                return self.insert_series(series)
        return False

    def insert_series(self, series):
        if series:
            series_collection = self.movie_db.series
            s = {
                'name': series['series_name'],
                'seasons': [
                    {
                        'season': series['series_season_number'],
                        'rating': series['series_rating']
                    }
                ],
                'rating': float(series['series_rating'])
            }
            series_collection.insert_one(s)
            return True
        return False

    def update_series(self, series, s):
        if series and s:
            size = len(s['seasons'])
            s['seasons'].append({'season': series['series_season_number'], 'rating': series['series_rating']})
            s['rating'] = (s['rating'] * size + float(series['series_rating'])) / (len(s['seasons'])*1.0)
            series_collection = self.movie_db.series
            query = {"_id": s['_id']}
            series_collection.find_one_and_replace(query, s)
            return True
        return False

    def find_series_by_id(self, series_id):
        if series_id:
            series_collection = self.movie_db.series
            series = series_collection.find_one({"_id": ObjectId(series_id)})
            return series
        return None

    def find_series_by_name(self, series_name):
        if series_name:
            series_collection = self.movie_db.series
            series = series_collection.find_one({"name": series_name})
            return series
        return None

    def delete_series_by_id(self, series_id):
        if series_id:
            series_collection = self.movie_db.series
            series_collection.delete_one({"_id": ObjectId(series_id)})
            return True
        return False

    def delete_all_series(self):
        series_collection = self.movie_db.series
        series_collection.delete_many()


if __name__ == '__main__':
    mongo = MongoDBClient()
    # mov = {'movie_name': 'the witcher: nightmare of the wolf', 'movie_rating': '3.5'}
    # mongo.insert_movie(mov)
    # mongo.delete_series_by_id("617f5955bb6fa79f38c2d5cf")
    # mongo.delete_series_by_id("617f55571a5a4f4ce163130a")
    # mongo.delete_all_series()
    # ser = {'series_name': 'avatar: the last airbender', 'series_season_number': '1 ', 'series_rating': '5'}
    # mongo.insert_or_update_series(ser)
    # ser = {'series_name': 'avatar: the last airbender', 'series_season_number': '2 ', 'series_rating': '5'}
    # mongo.insert_or_update_series(ser)
    m = mongo.find_movies_by_name('game')
    print(m)

