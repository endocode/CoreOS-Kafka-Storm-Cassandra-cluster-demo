#!/usr/bin/env bash

# Get running container's IP
IP=`hostname --ip-address | cut -f 1 -d ' '`
if [ $# == 2 ]; then SEEDS="$2,$IP";
else SEEDS="$IP"; fi

# Setup cluster name
if [ -z "$CASSANDRA_CLUSTERNAME" ]; then
        echo "No cluster name specified, preserving default one"
else
        sed -i -e "s/^cluster_name:.*/cluster_name: \"$CASSANDRA_CLUSTERNAME\"/" $CASSANDRA_CONFIG/cassandra.yaml
fi

# Dunno why zeroes here
sed -i -e "s/^rpc_address.*/rpc_address: \"$IP\"/" $CASSANDRA_CONFIG/cassandra.yaml

# Listen on IP:port of the container
sed -i -e "s/^listen_address.*/listen_address: \"$IP\"/" $CASSANDRA_CONFIG/cassandra.yaml

# Configure Cassandra seeds
if [ -z "$CASSANDRA_SEEDS" ]; then
	echo "No seeds specified, being my own seed..."
	CASSANDRA_SEEDS=$SEEDS
fi
sed -i -e "s/- seeds: \"127.0.0.1\"/- seeds: \"$CASSANDRA_SEEDS\"/" $CASSANDRA_CONFIG/cassandra.yaml

if [ -n "$BROADCAST_ADDR" ]; then
	sed -i -e "s/# broadcast_address: 1.2.3.4/broadcast_address: \"$BROADCAST_ADDR\"/g" $CASSANDRA_CONFIG/cassandra.yaml
fi

if [ -n "$CASSANDRA_SSL_STORAGE_PORT" ]; then
	sed -i -e "s/ssl_storage_port: .*/ssl_storage_port: $CASSANDRA_SSL_STORAGE_PORT/g" $CASSANDRA_CONFIG/cassandra.yaml
fi

if [ -n "$CASSANDRA_LOCAL_JMX" ]; then
	sed -i -e "s/\(^LOCAL_JMX=\).*/\1$CASSANDRA_LOCAL_JMX/g" $CASSANDRA_CONFIG/cassandra-env.sh
	PASSWORD=`openssl rand -base64 6`
	echo -e "\e[92mJMX credentials:\e[0m\n\e[92mUsername:\e[0m cassandra\n\e[92mPassword:\e[0m $PASSWORD"
	echo -e "monitorRole QED\ncontrolRole R&D\ncassandra $PASSWORD" > /etc/cassandra/jmxremote.password
	echo "cassandra     readwrite" >> /usr/lib/jvm/jre-7-oracle-x64/lib/management/jmxremote.access
	chown cassandra:cassandra /etc/cassandra/jmxremote.password
	chmod 400 /etc/cassandra/jmxremote.password
fi

## With virtual nodes disabled, we need to manually specify the token
#if [ -z "$CASSANDRA_TOKEN" ]; then
#	echo "Missing initial token for Cassandra"
#	exit -1
#fi
#
#echo "JVM_OPTS=\"\$JVM_OPTS -Dcassandra.initial_token=$CASSANDRA_TOKEN\"" >> $CASSANDRA_CONFIG/cassandra-env.sh

# Most likely not needed
echo "JVM_OPTS=\"\$JVM_OPTS -Djava.rmi.server.hostname=$IP\"" >> $CASSANDRA_CONFIG/cassandra-env.sh

echo "Starting Cassandra on $IP..."

cassandra -f
