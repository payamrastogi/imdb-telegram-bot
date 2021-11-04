#### Starting Zookeeper/kafka
- sudo ./kafka/bin/zookeeper-server-start.sh ./kafka/config/zookeeper.properties
- sudo ./kafka/bin/kafka-server-start.sh ./kafka/config/server.properties

#### Troubleshooting 
- Delete all files in kafka/data and kafka/logs folder
- List kafka topics
```
 ./kafka/bin/kafka-topics.sh --list --zookeeper 192.168.1.23:2181

```
- Describe a Kafka topic
```
./kafka/bin/kafka-topics.sh --describe --topic imdb_request_topic --bootstrap-server 192.168.1.23:9092
./kafka/bin/kafka-topics.sh --describe --topic psmdb_request_topic --bootstrap-server 192.168.1.23:9092
./kafka/bin/kafka-topics.sh --describe --topic response_topic --bootstrap-server 192.168.1.23:9092
```



#### References:
- https://stackoverflow.com/questions/19645527/trying-to-get-pycharm-to-work-keep-getting-no-python-interpreter-selected
- https://stackoverflow.com/questions/33785755/getting-could-not-find-function-xmlcheckversion-in-library-libxml2-is-libxml2
- https://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml
- https://stackoverflow.com/questions/59786719/how-can-i-access-yaml-data-from-a-python-file
- https://flexiple.com/check-if-list-is-empty-python/
- https://stackoverflow.com/questions/959215/how-do-i-remove-leading-whitespace-in-python
- https://dev.to/serhatteker/how-to-install-virtualenv-on-ubuntu-18-04-2jdi
- https://docs.python.org/2/library/re.html
- https://www.w3schools.com/python/ref_string_startswith.asp
- https://stackoverflow.com/questions/1549641/how-can-i-capitalize-the-first-letter-of-each-word-in-a-string
- https://stackoverflow.com/questions/3277503/how-to-read-a-file-line-by-line-into-a-list
- https://stackoverflow.com/questions/20510108/vertical-column-text-select-in-pycharm
- https://www.alcher.me/databases-ru-en/mongodb/install-32-and-64-mongodb/
- https://www.geeksforgeeks.org/mongodb-python-insert-update-data/
- https://docs.python.org/3/tutorial/classes.html
- https://www.geeksforgeeks.org/create-a-database-in-mongodb-using-python/
- https://www.w3schools.com/python/python_mongodb_create_db.asp
- https://docs.mongodb.com/manual/reference/method/db.removeUser/
- https://thedatafrog.com/en/articles/mongodb-remote-raspberry-pi/
- https://www.tutorialspoint.com/mongodb/mongodb_create_database.htm
- https://stackoverflow.com/questions/59481878/unable-to-start-kafka-with-zookeeper-kafka-common-inconsistentclusteridexceptio
- https://blog.fireheart.in/a?ID=01800-cdf8efa1-1f8b-4835-8aa1-bd4a89f66f81
- https://kafka.apache.org/quickstart
- https://stackoverflow.com/questions/62405458/unable-to-send-messages-to-topic-in-kafka-python

