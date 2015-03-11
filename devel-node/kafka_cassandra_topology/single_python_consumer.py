#!/usr/bin/env python
import threading, logging, time

import yaml
import uuid
from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer

from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from cassandra.query import BatchStatement

cluster = Cluster(['172.17.8.101','172.17.8.102','172.17.8.103'])
session = cluster.connect()

class Consumer(threading.Thread):
    daemon = True

    def run(self):
        client = KafkaClient("172.17.8.101:9092")
        consumer = SimpleConsumer(client, "test-group", "topic")

        batch_size = 300
        global_counter = 0
        counter = 0
        batch = BatchStatement()

        for message in consumer:
            if counter >= batch_size:
                 session.execute(batch)
                 batch = BatchStatement()
                 counter = 0

            temp = yaml.load(message[1][3])
#            print temp
            global_counter += 1
            print global_counter
            prepared = session.prepare("""
                    INSERT INTO testkeyspace.meter_data (timestamp, id, P_1, P_2, P_3, Q_1, Q_2, Q_3)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """)
            batch.add(prepared, (temp["timestamp"], uuid.UUID(temp["id"]), temp["P_1"], temp["P_2"], temp["P_3"], temp["Q_1"], temp["Q_2"], temp["Q_3"]))
            counter += 1

#            session.execute(prepared, (1425398075000, uuid.UUID('f21d2312-ba1b-4d2c-8cfa-817bf783cbe6'), 1,2,3,4,5,6))
#            keys = ",".join(temp.iterkeys())
#            values = ",".join(temp.itervalues())
#            print "INSERT INTO testkeyspace.meter_data (%s) VALUES(%s)" % (keys, values)
#            session.execute("INSERT INTO testkeyspace.meter_data (%s) VALUES(%s)" % (keys, values))

def main():
    threads = [
        Consumer()
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
