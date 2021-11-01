from kafka import KafkaConsumer
consumer = KafkaConsumer('sample', bootstrap_servers='192.168.1.23:9092')
for message in consumer:
    print(message)



