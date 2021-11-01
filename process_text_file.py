import re


class ProcessTextFile:

    def __init__(self, filename):
        self.filename = filename

    def process_file(self):
        with open(self.filename) as file:
            for line in file:
                line = line.strip().lower()
                if self.is_series(line):
                    print(self.get_series_details(line))
                else:
                    print(self.get_movie_details(line))

    @staticmethod
    def is_series(text):
        if text.startswith("series:"):
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
    parse = Parse('movies.txt')
    parse.process_file()
