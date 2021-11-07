from kafka import KafkaProducer
import json
from bson import json_util

kafka_producer = KafkaProducer(bootstrap_servers='192.168.1.23:9092')
request = {
    'name': 'Ravi',
    'age': 18
}
kafka_producer.send('sample', json.dumps(request, default=json_util.default).encode('utf-8'))
kafka_producer.flush()
