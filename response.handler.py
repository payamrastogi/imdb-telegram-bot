import json

import telepot  # Importing the telepot library
from kafka import KafkaConsumer

import config_util

RESPONSE_TOPIC = config_util.read_response_topic()
BOOTSTRAP_SERVERS = config_util.read_bootstrap_servers()


class ResponseHandler:
    def __init__(self):
        self.bot = telepot.Bot(config_util.read_telegram_bot_token())

    def start(self):
        print("start")
        kafka_consumer = KafkaConsumer(RESPONSE_TOPIC,
                                       bootstrap_servers=BOOTSTRAP_SERVERS,
                                       value_deserializer=lambda m: json.loads(m.decode('utf-8')))
        for response in kafka_consumer:
            self.process_response(response)

    def process_response(self, response):
        response = response.value
        print(response)
        chat_id = response["chat_id"]
        message = ""
        data = response["data"]
        print(data)
        for key in data:
            message = message + "\n" + str(key) + ": " + str(data[key])
        self.send_message(chat_id, message)

    def send_message(self, chat_id, message):
        self.bot.sendMessage(chat_id, message)


if __name__ == '__main__':
    response_handler = ResponseHandler()
    response_handler.start()
