import threading

from kafka import KafkaProducer, KafkaConsumer
import json

import time

from kafka.errors import NoBrokersAvailable


class Consumer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        consumer = KafkaConsumer(bootstrap_servers='kafka:9092',
                                 auto_offset_reset='earliest',
                                 consumer_timeout_ms=1000)
        consumer.subscribe(['registered_user'])

        while not self.stop_event.is_set():
            for message in consumer:
                print(message)
                if self.stop_event.is_set():
                    break

        consumer.close()


class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers="kafka:9092", value_serializer=json_serializer)

        while not self.stop_event.is_set():
            producer.send('my-topic', {"user": "Max"})
            time.sleep(1)

        producer.close()


def json_serializer(data):
    return json.dumps(data).encode("utf-8")


while True:
    try:
        producer = KafkaProducer(bootstrap_servers="kafka:9092", value_serializer=json_serializer)
        break
    except NoBrokersAvailable as err:
        print(f"Unable to find a broker: {err}")
        time.sleep(1)

print("Connected!")

if __name__ == '__main__':
    Producer().start()
    Consumer().start()
