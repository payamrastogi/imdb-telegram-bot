import yaml

with open('config.yaml') as f:
    config_yaml = yaml.load(f, Loader=yaml.FullLoader)


def read_general_request_topic():
    return config_yaml['general_request_topic']


def read_imdb_request_topic():
    return config_yaml['imdb_request_topic']


def read_psmdb_request_topic():
    return config_yaml['psmdb_request_topic']


def read_response_topic():
    return config_yaml['response_topic']


def read_bootstrap_servers():
    return config_yaml['bootstrap_servers']


def read_telegram_bot_token():
    return config_yaml['bot_token']


def read_mongo_uri():
    return config_yaml['mongo_uri']
