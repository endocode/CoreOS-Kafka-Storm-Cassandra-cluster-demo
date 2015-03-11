FROM ubuntu:trusty
# based on Spotify's dockerfile - https://github.com/spotify/docker-cassandra/blob/master/cassandra-base/Dockerfile
MAINTAINER Anton Khramov <anton@endocode.com>

RUN /bin/echo -e "deb http://archive.ubuntu.com/ubuntu/ trusty multiverse\ndeb http://archive.ubuntu.com/ubuntu/ trusty-updates multiverse\ndeb http://security.ubuntu.com/ubuntu trusty-security multiverse" | tee -a /etc/apt/sources.list
RUN apt-get update && apt-get dist-upgrade -y
RUN apt-get install -y expect java-package
RUN curl -j -L -H 'Cookie: oraclelicense=accept-securebackup-cookie' https://edelivery.oracle.com/otn-pub/java/jdk/7u79-b15/jre-7u79-linux-x64.tar.gz -o /tmp/jre-7u79-linux-x64.tar.gz
ADD expect /tmp/expect
RUN /tmp/expect

ADD cassandra_repo_key /tmp/cassandra_repo_key
RUN apt-key add /tmp/cassandra_repo_key
RUN echo "deb http://debian.datastax.com/community stable main" | tee -a /etc/apt/sources.list.d/cassandra.sources.list
RUN apt-get update
RUN dpkg -i /tmp/oracle-java7-jre_7u79_amd64.deb || apt-get install -fy

# Workaround for https://github.com/docker/docker/issues/6345
RUN ln -s -f /bin/true /usr/bin/chfn

# Install Cassandra 2.0.14
RUN apt-get install -y cassandra=2.0.14 dsc20=2.0.14-1

# cleanup image
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

ENV CASSANDRA_CONFIG /etc/cassandra

# Necessary since cassandra is trying to override the system limitations
# See https://groups.google.com/forum/#!msg/docker-dev/8TM_jLGpRKU/dewIQhcs7oAJ
RUN rm -f /etc/security/limits.d/cassandra.conf

#JMX port
EXPOSE 7199
#storage_port
EXPOSE 7000
#ssl_storage_port (prev 7001 conflicts with etcd)
EXPOSE 7002
#rpc_port
EXPOSE 9160
#native_transport_port
EXPOSE 9042
#Hadoop Job Tracker client port
#EXPOSE 8012
#OpsCenter agent port
#EXPOSE 61621

# Place cluster-node startup-config script
ADD cassandra-clusternode.sh /usr/local/bin/cassandra-clusternode

# Fix to solve "JNA not found. Native methods will be disabled."
RUN ln -s /usr/share/java/jna-*.jar /usr/share/cassandra/lib/

RUN mkdir -p /var/lib/cassandra/data /var/lib/cassandra/commitlog /var/lib/cassandra/saved_caches

# Start Cassandra
ENTRYPOINT ["cassandra-clusternode"]
