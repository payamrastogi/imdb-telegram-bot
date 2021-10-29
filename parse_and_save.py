import re


def process_file(filename):
    with open(filename) as file:
        for line in file:
            line = line.strip().lower()
            if is_series(line):
                print(get_series_details(line))
            else:
                print(get_movie_details(line))


def is_series(text):
    if text.startswith("series:"):
        return True
    else:
        return False


def get_series_details(text):
    text = text.strip().lower()
    series_name = get_series_name(text)
    series_season_number = get_series_season_number(text)
    series_rating = get_series_rating(text)
    return {'series_name': series_name, 'series_season_number': series_season_number, 'series_rating': series_rating}


def get_series_name(text):
    text = text.strip().lower()
    series_name = re.search('series:[0-9 ]*([a-z0-9:.%,&\\- ]*)season:[0-9 ]*[0-9.() ]*', text)
    if series_name:
        return series_name.group(1).strip()
    else:
        return None


def get_series_rating(text):
    text = text.strip().lower()
    series_rating = re.search('series:[0-9 ]*[a-z0-9:.%,&\\- ]*season:[0-9 ]*[(]*([0-9.]*)[)]*', text)
    if series_rating:
        return series_rating.group(1)
    else:
        return None


def get_series_season_number(text):
    text = text.strip().lower()
    series_season_number = re.search('series:[0-9 ]*[a-z0-9:.%,&\\- ]*season:([0-9 ]*)[0-9.() ]*', text)
    if series_season_number:
        return series_season_number.group(1)
    else:
        return None


def get_movie_details(text):
    text = text.strip().lower()
    movie_name = get_movie_name(text)
    movie_rating = get_movie_rating(text)
    return {'movie_name': movie_name, 'movie_rating': movie_rating}


def get_movie_name(text):
    text = text.strip().lower()
    movie_name = re.search('([a-z0-9:.%,&\\- ]*)[(]?[0-9.]*[)]?', text)
    if movie_name:
        return movie_name.group(1).strip()
    else:
        return None


def get_movie_rating(text):
    text = text.strip().lower()
    movie_rating = re.search('[a-z0-9:.%,&\\- ]*[(]?([0-9.]*)[ )]?', text)
    if movie_rating:
        return movie_rating.group(1)
    else:
        return None


if __name__ == '__main__':
    # search_movies_by_name('dune')
    # name = get_series_name('Series: Justice league season:2')
    # print(name)
    # name = get_series_name('Series: Breaking Bad season:1 (5)  ')
    # print(name)
    # rating = get_series_rating('Series: Justice league season:2')
    # print(rating)
    # rating = get_series_rating('Series: Breaking Bad season:1 (5)  ')
    # print(rating)
    # season = get_series_season_number('Series: Justice league season:2')
    # print(season)
    # season = get_series_season_number('Series: Breaking Bad season:1 (5)  ')
    # print(season)
    # print(get_series_details('Series: Justice league season:2'))
    process_file('movies.txt')
