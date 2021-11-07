from kafka import KafkaConsumer
import config_util
BOOTSTRAP_SERVERS = config_util.read_bootstrap_servers()

kafka_consumer = KafkaConsumer("sample", bootstrap_servers=BOOTSTRAP_SERVERS)
for request in kafka_consumer:
    print(request)