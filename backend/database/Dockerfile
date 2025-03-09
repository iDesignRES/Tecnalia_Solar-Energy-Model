FROM mysql:8.0.25

ADD startupscripts/. /docker-entrypoint-initdb.d
ADD cnf/. /etc/mysql/conf.d/
RUN chmod -R 644 /etc/mysql/conf.d/*