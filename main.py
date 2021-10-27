from imdb import IMDb, IMDbError
import yaml

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


def read_telegram_bot_token():
    with open('telegram_token.yaml') as f:
        telegram_bot_token_yaml = yaml.load(f, Loader=yaml.FullLoader)
        return telegram_bot_token_yaml['bot_token']


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # search_movies_by_name('dune')
    read_telegram_bot_token()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
