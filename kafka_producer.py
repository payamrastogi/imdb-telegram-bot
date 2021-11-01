from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers='192.168.1.23:9092')
producer.send('sample', b'Hello, World!')
producer.flush()
# for e in range(1000):
#     data = {'number' : e}
#     producer.send('numtest', value=data)

# bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic sample --from-beginning