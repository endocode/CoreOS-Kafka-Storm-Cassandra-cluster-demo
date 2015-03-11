FROM endocode/storm:0.9.2
MAINTAINER Anton Khramov <anton@endocode.com>

RUN /usr/bin/config-supervisord.sh nimbus
RUN /usr/bin/config-supervisord.sh drpc

# nimbus.thrift.port
EXPOSE 6627
# drpc.port
EXPOSE 3772
# drpc.invocations.port
EXPOSE 3773

CMD /usr/bin/start-supervisor.sh
