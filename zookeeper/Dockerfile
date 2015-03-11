FROM ubuntu:trusty
MAINTAINER Anton Khramov <anton@endocode.com>

RUN apt-get update && apt-get dist-upgrade -y
RUN apt-get install -y zookeeper

# cleanup image
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN sed -i 's/ROLLINGFILE/CONSOLE/' /etc/zookeeper/conf/environment
ADD start.sh /usr/local/bin/

VOLUME /var/lib/zookeeper

# Zookeeper client port
EXPOSE 2181
# Zookeeper peer port
EXPOSE 2888
# Zookeeper leader (election) port
EXPOSE 3888

CMD ["/usr/local/bin/start.sh"]
