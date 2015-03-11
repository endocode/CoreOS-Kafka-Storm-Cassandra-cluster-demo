import logging
import yaml
import uuid

from pyleus.storm import SimpleBolt

log = logging.getLogger('cassandra_writer')

from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

cluster = Cluster(['172.17.8.101','172.17.8.102','172.17.8.103'])
session = cluster.connect()

class CassandraWriter(SimpleBolt):
    def process_tuple(self, tup):
        line, = tup.values
        data = yaml.load(line)
        prepared = session.prepare("""
               INSERT INTO testkeyspace.meter_data (timestamp, id, P_1, P_2, P_3, Q_1, Q_2, Q_3)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)
               """)
        session.execute(prepared, (data["timestamp"], uuid.UUID(data["id"]), data["P_1"], data["P_2"], data["P_3"], data["Q_1"], data["Q_2"], data["Q_3"]))

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.DEBUG,
        filename='/tmp/cassandra_writer.log',
        format="%(message)s",
        filemode='a',
    )
    CassandraWriter().run()
