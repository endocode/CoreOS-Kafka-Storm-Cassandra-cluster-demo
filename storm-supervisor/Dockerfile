FROM endocode/storm:0.9.2
MAINTAINER Anton Khramov <anton@endocode.com>

# worker 1 port
EXPOSE 6700
# worker 2 port
EXPOSE 6701
# worker 3 port
EXPOSE 6702
# worker 4 port
EXPOSE 6703
# logviewer port
EXPOSE 8000

RUN /usr/bin/config-supervisord.sh supervisor
RUN /usr/bin/config-supervisord.sh logviewer

CMD /usr/bin/start-supervisor.sh
