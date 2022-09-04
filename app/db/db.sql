CREATE DATABASE app;
CREATE USER app WITH PASSWORD 'top_secret';
ALTER ROLE app SET client_encoding TO 'utf8';
ALTER ROLE app SET default_transaction_isolation TO 'read committed';
ALTER ROLE app SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE app TO app;