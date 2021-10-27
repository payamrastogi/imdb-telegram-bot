import datetime  # Importing the datetime library
import telepot  # Importing the telepot library
from telepot.loop import MessageLoop  # Library function to communicate with telegram bot
from time import sleep  # Importing the time library to provide the delays in program
from imdb import IMDb, IMDbError

now = datetime.datetime.now()  # Getting date and time

def handle(msg):
    chat_id = msg['chat']['id']  # Receiving the message from telegram
    command = msg['text']  # Getting text from the message

    print('Received:')
    print(command)

    # Comparing the incoming message to send a reply according to it
    if command == '/hi':
        bot.sendMessage(chat_id, str("Hi! from crunch"))
    elif command == '/time':
        bot.sendMessage(chat_id,
                        str("Time: ") + str(now.hour) + str(":") + str(now.minute) + str(":") + str(now.second))
    elif command == '/date':
        bot.sendMessage(chat_id, str("Date: ") + str(now.day) + str("/") + str(now.month) + str("/") + str(now.year))
    elif '/movie' in command:
        movie = command.split(' ', 1)
        print(movie[0]+":"+movie[1])
        search_movies_by_name(chat_id, movie[1])

def search_movies_by_name(chat_id, name):
    ia = IMDb()
    try:
        movies = ia.search_movie(name)
        for movie in movies:
            try:
                # print(movie.movieID)
                mov = ia.get_movie(movie.movieID)
                #print(movie, , mov.data['rating'], mov.data['genres'])

                bot.sendMessage(chat_id,
                                str(mov.data['title']) + str("\n")
                                + str(mov.data['year']) + str("\n")
                                + str(mov.data['rating']) + str("\n")
                                + str(mov.data['genres']))
                #mov.infoset2keys
                #print(mov.get('plot'))
            except (IMDbError, KeyError) as err:
                pass
                # print(err)
    except IMDbError as e:
        print(e)



# Insert your telegram token below
bot = telepot.Bot('telegram_token')
print(bot.getMe())

# Start listening to the telegram bot and whenever a message is  received, the handle function will be called.
MessageLoop(bot, handle).run_as_thread()
print('Listening....')

while 1:
    sleep(10)
