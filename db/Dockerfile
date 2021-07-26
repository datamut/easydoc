FROM postgres:13.3-alpine3.14

ARG DB_PASSWORD

COPY init.sql .

# substitute the DB_PASSWORD placeolder in the init.sql
RUN sed -i "s/__DB_PASSWORD_PLACEHOLDER__/${DB_PASSWORD}/g" init.sql

RUN cp init.sql /docker-entrypoint-initdb.d/
