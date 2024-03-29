import pymongo
from bson import ObjectId
import config_util


class MongoDBClient:
    def __init__(self):
        try:
            self.mongo_client = pymongo.MongoClient(config_util.read_mongo_uri())
            self.movie_db = self.mongo_client["moviedb"]
            self.movies_collection = self.movie_db.movies
            self.series_collection = self.movie_db.series
            self.recommendations_collection = self.movie_db.recommendations
        except Exception as e:
            print("could not connect to MongoDB", e)

    def insert_movie(self, movie):
        if movie:
            mov = {'name': movie['movie_name'], 'rating': movie['movie_rating']}
            self.movies_collection.insert_one(mov)
            return True
        return False

    def find_movies_by_name(self, movie_name):
        movies = []
        if movie_name:
            res = self.movies_collection.find({'name': {'$regex': movie_name.strip().lower(), '$options': 'i'}})
            for movie in res:
                movies.append({"psmdb_id": str(movie["_id"]), "name": movie["name"], "psmdb_rating": movie["rating"]})
        return movies

    def find_movie_by_id(self, movie_id):
        if movie_id:
            movie = self.movies_collection.find_one({"_id": ObjectId(movie_id)})
            return movie
        return None

    def find_movies_by_rating_gte(self, rating):
        movies = []
        if rating:
            res = self.movies_collection.find({"rating": {"$gte": "rating"}})
            for movie in res:
                movies.append({"psmdb_id": str(movie["_id"]), "name": movie["name"], "psmdb_rating": movie["rating"]})
            return movies
        return []

    def update_movie_imdb_id(self, psmdb_id, imdb_id):
        if psmdb_id and imdb_id:
            movie = self.find_movie_by_id(psmdb_id)
            movie["imdb_id"] = imdb_id
            query = {"_id": movie['_id']}
            self.movies_collection.find_one_and_replace(query, movie)
            return True
        return False

    def delete_movie_by_id(self, movie_id):
        if movie_id:
            self.movies_collection.delete_one({"_id": ObjectId(movie_id)})
            return True
        return False

    def delete_all_movies(self):
        self.movies_collection.drop()

    def insert_or_update_series(self, series):
        print("insert or update", series)
        if series:
            s = self.find_series_by_name(series['series_name'].lower())
            print("----", s)
            if s:
                return self.update_series(series, s)
            else:
                return self.insert_series(series)
        return False

    def insert_series(self, series):
        if series:
            s = {
                'name': series['series_name'].lower(),
                'seasons': [
                    {
                        'season': series['series_season_number'],
                        'rating': series['series_rating']
                    }
                ],
                'rating': float(series['series_rating'])
            }
            self.series_collection.insert_one(s)
            return True
        return False

    def update_series(self, series, s):
        if series and s:
            size = len(s['seasons'])
            s['seasons'].append({'season': series['series_season_number'], 'rating': series['series_rating']})
            s['rating'] = (s['rating'] * size + float(series['series_rating'])) / (len(s['seasons']) * 1.0)
            query = {"_id": s['_id']}
            self.series_collection.find_one_and_replace(query, s)
            return True
        return False

    def find_series_by_id(self, series_id):
        if series_id:
            series = self.series_collection.find_one({"_id": ObjectId(series_id)})
            return series
        return None

    def find_series_by_name(self, series_name):
        if series_name:
            series = self.series_collection.find_one({"name": series_name.lower()})
            return series
        return None

    def delete_series_by_id(self, series_id):
        if series_id:
            self.series_collection.delete_one({"_id": ObjectId(series_id)})
            return True
        return False

    def delete_all_series(self):
        self.series_collection.drop()

    def insert_movie_recommendation(self, movie):
        if movie:
            mov = self.find_movie_by_imdb_id(movie["imdb_id"])
            if not mov:
                self.recommendations_collection.insert_one(movie)
            return True
        return False

    def find_movie_by_imdb_id(self, imdb_id):
        if imdb_id:
            movie = self.recommendations_collection.find_one({"imdb_id": imdb_id})
            return movie
        return None


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
    # print(mongo.delete_movie_by_id("6188c31dd15654a4dd8b0e01"))
    # print(mongo.delete_movie_by_id("6188c4fe5dc7aed6942e0bb3"))
    # print(mongo.delete_movie_by_id("6188c5865dc7aed6942e0bb4"))
    # print(mongo.delete_movie_by_id("6188c5c9ec807cdcf6aa4570"))
    # print(mongo.delete_movie_by_id("6188c5f938222f44c4e04aa8"))
    # print(mongo.delete_movie_by_id("6188c654af22330e6383d47c"))
    # print(mongo.delete_movie_by_id("6188c6ad7d1a9f9d4a02ffd0"))

