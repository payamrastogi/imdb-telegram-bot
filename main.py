from imdb import IMDb, IMDbError

ia = IMDb()


def search_movies_by_name(name):
    try:
        movies = ia.search_movie(name)
        for movie in movies:
            try:
                # print(movie.movieID)
                mov = ia.get_movie(movie.movieID)
                print(movie, mov.data['year'], mov.data['rating'], mov.data['genres'])
                mov.infoset2keys
                print(mov.get('plot'))
            except (IMDbError, KeyError) as err:
                pass
                # print(err)
    except IMDbError as e:
        print(e)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    search_movies_by_name('dune')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
