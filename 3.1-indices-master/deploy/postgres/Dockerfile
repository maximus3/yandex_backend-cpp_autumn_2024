FROM postgres:15

ENV POSTGRES_USER="user" POSTGRES_PASSWORD="random" POSTGRES_DB="homework"

ADD ./deploy/postgres/init-user-db.sh /docker-entrypoint-initdb.d/init-user-db.sh
ADD ./deploy/postgres/dump.sql /tmp/dump.sql
