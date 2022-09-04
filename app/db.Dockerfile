# Base image
FROM postgres:14.5 AS postgres-test

# Create app directory
RUN apt-get update && apt-get install -y postgis && apt-get install -y postgresql-14-postgis-3

COPY ./db/db.sql /docker-entrypoint-initdb.d/