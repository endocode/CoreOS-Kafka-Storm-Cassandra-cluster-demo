##CoreOS instances

Install Vagrant (>= 1.6) and VirtualBox, then run

```
git clone https://github.com/endocode/CoreOS-Kafka-Storm-Cassandra-cluster-demo
cd CoreOS-Kafka-Storm-Cassandra-cluster-demo/coreos-vagrant
vagrant up
```

Vagrant will create three CoreOS VMs with the following IPs: 172.17.8.101, 172.17.8.102, 172.17.8.103

Then login to your first Vagrant instance and submit fleet units:
```
vagrant ssh core-01
fleetctl submit /tmp/fleet/*
```

##Run Zookeeper cluster

```
fleetctl start zookeeper@{1..3}.service
```

##Run Kafka cluster

```
fleetctl start kafka@{1..3}.service
```

##Run Cassandra luster

```
fleetctl start cassandra@{1..3}.service
```

##Run Storm cluster

```
fleetctl start storm-nimbus.service
# storm-ui (not required) will listen on http://172.17.8.101:8080
fleetctl start storm-ui.service
fleetctl start storm-supervisor@{1..3}.service
```

##Run development container inside CoreOS VM (storm, kafka, maven, scala, python, zookeeper, cassandra, etc)

```docker run --rm -ti -v /home/core/devel:/root/devel -e BROKER_LIST=`fleetctl list-machines -no-legend=true -fields=ip | sed 's/$/:9092/' | tr '\n' ','` -e NIMBUS_HOST=`etcdctl get /storm-nimbus` -e ZK=`fleetctl list-machines -no-legend=true -fields=ip | tr '\n' ','` endocode/devel-node:0.9.2 start-shell.sh bash```

###Test Kafka cluster

Run these commands in devel-node container to test your Kafka cluster.

Create topic

```$KAFKA_HOME/bin/kafka-topics.sh --create --topic test --partitions 3 --zookeeper $ZK --replication-factor 2```

Show topic info

```$KAFKA_HOME/bin/kafka-topics.sh --describe --topic test --zookeeper $ZK```

Send some data to topic

```$KAFKA_HOME/bin/kafka-console-producer.sh --topic test --broker-list="$BROKER_LIST"```

Get some data from topic

```$KAFKA_HOME/bin/kafka-console-consumer.sh --zookeeper $ZK --topic test --from-beginning```

Remove topic (valid only with KAFKA_DELETE_TOPIC_ENABLE=true environment)

```$KAFKA_HOME/bin/kafka-topics.sh --zookeeper $ZK --delete --topic test```

###Cassandra

####Show Cassandra cluster status

```nodetool -h172.17.8.101 status```

####Cassandra cluster CLI


```cqlsh 172.17.8.101```

####Cassandra queries

You can view and manage your Cassandra table's content with the following queries:

```
SELECT * FROM testkeyspace.meter_data;
#Delete content from table
TRUNCATE testkeyspace.meter_data;
SELECT COUNT(*) FROM testkeyspace.meter_data LIMIT 1000000;
```

####Storm topology

We will use Pyleus (http://yelp.github.io/pyleus/) framework to manage Storm topologies in pure python. Unfortunately current Pyleus version (0.2.4) doesn't support latest Storm 0.9.3 (https://github.com/Yelp/pyleus/issues/86). That is why we use Storm 0.9.2 in this example.
endocode/devel-node:0.9.2 Docker container contains sample kafka-storm-cassandra Storm topology. Follow these steps to build and submit Storm topology into Storm cluster:

```
docker run --rm -ti -v /home/core/devel:/root/devel -e BROKER_LIST=`fleetctl list-machines -no-legend=true -fields=ip | sed 's/$/:9092/' | tr '\n' ','` -e NIMBUS_HOST=`etcdctl get /storm-nimbus` -e ZK=`fleetctl list-machines -no-legend=true -fields=ip | tr '\n' ','` endocode/devel-node:0.9.2 start-shell.sh bash
# Create Kafka topic
$KAFKA_HOME/bin/kafka-topics.sh --create --topic topic --partitions 3 --zookeeper $ZK --replication-factor 2
# Create Cassandra keyspace and table
echo "CREATE KEYSPACE testkeyspace WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 2 };" | cqlsh 172.17.8.101
echo "CREATE TABLE IF NOT EXISTS testkeyspace.meter_data ( id uuid, Timestamp timestamp, P_1 float, P_2 float, P_3 float, Q_1 float, Q_2 float, Q_3 float, HARM list<int>, PRIMARY KEY (id, Timestamp) );" | cqlsh 172.17.8.101
cd ~/kafka_cassandra_topology
pyleus build
pyleus submit -n $NIMBUS_HOST kafka-cassandra.jar
#Run Kafka random data producer
./single_python_producer.py
```

It will run kafka-cassandra topology in Storm cluster and Kafka producer. All this data will be stored in Cassandra cluster using Storm topology. You can monitor Cassandra table in CQL shell in another endocode/devel-node:0.9.2 container:

```
cqlsh 172.17.8.101
Connected to cluster at 172.17.8.101:9160.
[cqlsh 4.1.1 | Cassandra 2.0.12 | CQL spec 3.1.1 | Thrift protocol 19.39.0]
Use HELP for help.
cqlsh> SELECT COUNT(*) FROM testkeyspace.meter_data LIMIT 1000000;

 count
-------
  1175

(1 rows)

cqlsh>
```
