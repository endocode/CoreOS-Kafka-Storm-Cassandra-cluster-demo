#!/usr/bin/env python
import threading, logging, time

import time
import json
import uuid
from random import randint
from kafka.client import KafkaClient
from kafka.producer import SimpleProducer

def rand():
   return float("%d.%.3d" % (randint(0,999), randint(0,999)))

class Producer(threading.Thread):
    daemon = True

    def run(self):
        client = KafkaClient("172.17.8.101:9092")
        producer = SimpleProducer(client)
        global_counter = 0

        while True:
            dict = {'P_1': rand(), 'P_2': rand(), 'P_3': rand(), 'Q_1': rand(), 'Q_2': rand(), 'Q_3': rand(), 'timestamp': int(time.time())*1000, 'id': str(uuid.uuid4())};
            producer.send_messages('topic', json.dumps(dict))
            global_counter += 1
            print global_counter

def main():
    threads = [
        Producer(),
    ]

    for t in threads:
        t.start()

    while True:
        pass

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.DEBUG
        )
    main()
