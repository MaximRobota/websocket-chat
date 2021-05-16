import json
import time
import uuid

import requests
from kafka.admin import NewTopic
from loguru import logger
from kafka import KafkaProducer, KafkaConsumer, KafkaAdminClient
from kafka.errors import NoBrokersAvailable

BOOTSTRAP_SERVERS = 'kafka:9092'
OUTBOUND_TOPIC_NAME = 'persisted_message'
INBOUND_TOPIC_NAME = 'new_message'


def json_serializer(data):
    return json.dumps(data).encode('utf-8')


def create_topic():
    while True:
        try:
            admin_client = KafkaAdminClient(
                bootstrap_servers=BOOTSTRAP_SERVERS,
                client_id='mps_admin'
            )
            break
        except:
            logger.exception(f'Could not connect to Kafka at {BOOTSTRAP_SERVERS}')
            time.sleep(1)

    topic_list = [NewTopic(name=OUTBOUND_TOPIC_NAME, num_partitions=1, replication_factor=1)]
    logger.info(f'Topics List {admin_client.list_topics()}')
    admin_client.create_topics(new_topics=topic_list, validate_only=False)
    logger.info(f'Created topic: {OUTBOUND_TOPIC_NAME}')


def create_producer():
    return KafkaProducer(bootstrap_servers=BOOTSTRAP_SERVERS, value_serializer=json_serializer)


def create_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                bootstrap_servers=BOOTSTRAP_SERVERS,
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
                # auto_offset_reset='earliest',
                # consumer_timeout_ms=1000
            )
            consumer.subscribe([INBOUND_TOPIC_NAME])
            return consumer
        except NoBrokersAvailable:
            logger.info('Could not connect to consumer')
            time.sleep(1)


def save_msg_to_db(data):
    logger.info(f'data {data}')

    try:
        resp_status = requests.post(
            'http://identity-service:80/message', data["data"],
            headers=data['headers']
        )
        logger.info(f'resp_status {resp_status.status_code}')
        if resp_status.status_code == 200:
            return resp_status
        else:
            return False
    except Exception as e:
        return logger.info('Could not connect to Identity service ', e)


if __name__ == '__main__':
    create_topic()
    producer = create_producer()
    consumer = create_consumer()
    logger.info('Got Consumer!')
    for msg in consumer:
        logger.info(f'Got msg: {msg}')
        dataValue = msg.value
        # dataValue['data']['_uuid'] = uuid.uuid1()
        dataValue['data']['_uuid'] = 'qwqeqweqweqweqwe'

        resp_status = save_msg_to_db(dataValue)

        logger.info(f"resp_status {resp_status}")

        if resp_status:
            producer.send(OUTBOUND_TOPIC_NAME, resp_status)
            logger.info(f"Sent message to topic (MS => WS) {OUTBOUND_TOPIC_NAME!r} {resp_status}")
        else:
            logger.info('Failed to send message to topic')


