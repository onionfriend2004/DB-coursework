FROM mysql:latest

ENV MYSQL_ALLOW_EMPTY_PASSWORD=yes
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=password
ENV MYSQL_DATABASE=database

COPY ./migrations/init.sql /docker-entrypoint-initdb.d/01-init.sql
COPY ./migrations/seed_data.sql /docker-entrypoint-initdb.d/02-seed_data.sql

ADD ./sql.cnf /etc/mysql/conf.d/