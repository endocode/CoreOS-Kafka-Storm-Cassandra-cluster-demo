FROM endocode/storm:0.9.2
MAINTAINER Anton Khramov <anton@endocode.com>

# web interface port
EXPOSE 8080

RUN /usr/bin/config-supervisord.sh ui
CMD /usr/bin/start-supervisor.sh
