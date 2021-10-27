# !/usr/bin/env python3
import datetime  # Importing the datetime library
import telepot  # Importing the telepot library
from telepot.loop import MessageLoop  # Library function to communicate with telegram bot
from time import sleep  # Importing the time library to provide the delays in program
from imdb import IMDb, IMDbError
import yaml

now = datetime.datetime.now()  # Getting date and time


def read_telegram_bot_token():
    with open('telegram_token.yaml') as f:
        telegram_bot_token_yaml = yaml.load(f, Loader=yaml.FullLoader)
        return telegram_bot_token_yaml['bot_token']

def handle(msg):
    chat_id = msg['chat']['id']  # Receiving the message from telegram
    command = msg['text']  # Getting text from the message

    print('Received:')
    print(command)

    # Comparing the incoming message to send a reply according to it
    if command == '/hi':
        bot.sendMessage(chat_id, str("Hi! from crunch"))
    elif command == '/help':
        bot.sendMessage(chat_id, str("[/search <movie_name>] returns rating, year, and genres"))
    elif command == '/time':
        bot.sendMessage(chat_id,
                        str("Time: ") + str(now.hour) + str(":") + str(now.minute) + str(":") + str(now.second))
    elif command == '/date':
        bot.sendMessage(chat_id, str("Date: ") + str(now.day) + str("/") + str(now.month) + str("/") + str(now.year))
    elif '/search' in command:
        search = command.split("/search", 1)
        if not search and len(search) == 2:
            search_movies_by_name(chat_id, search[1].lstrip())


def search_movies_by_name(chat_id, name):
    ia = IMDb()
    try:
        movies = ia.search_movie(name)
        for movie in movies:
            try:
                # print(movie.movieID)
                mov = ia.get_movie(movie.movieID)
                # print(movie, , mov.data['rating'], mov.data['genres'])

                bot.sendMessage(chat_id,
                                str("Id:") + str(movie.movieID) + str("\n")
                                + str("Title: ") + str(mov.data['title']) + str("\n")
                                + str("Year: ") + str(mov.data['year']) + str("\n")
                                + str("Rating: ") + str(mov.data['rating']) + str("\n")
                                + str("Genres: ") + str(mov.data['genres']))
                # mov.infoset2keys
                # print(mov.get('plot'))
            except (IMDbError, KeyError) as err:
                pass
                # print(err)
    except IMDbError as e:
        print(e)


# Insert your telegram token below
bot = telepot.Bot(read_telegram_bot_token())
print(bot.getMe())

# Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
MessageLoop(bot, handle).run_as_thread()
print('Listening....')

while 1:
    sleep(10)
