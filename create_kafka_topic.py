from kafka.admin import KafkaAdminClient, NewTopic

admin_client = KafkaAdminClient(
    bootstrap_servers="192.168.1.23:9092",
    client_id='imdb-telegram-bot'
)

topic_list = [NewTopic(name="imdb_request_topic", num_partitions=1, replication_factor=1),
              NewTopic(name="psmdb_request_topic", num_partitions=1, replication_factor=1),
              NewTopic(name="general_request_topic", num_partitions=1, replication_factor=1),
              NewTopic(name="recommendation_topic", num_partitions=1, replication_factor=1),
              NewTopic(name="response_topic", num_partitions=1, replication_factor=1)]
admin_client.create_topics(new_topics=topic_list, validate_only=False)

