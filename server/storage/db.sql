CREATE TABLE IF NOT EXISTS clients
(
client_id  serial PRIMARY KEY,
username varchar NOT null,
uniq_id varchar NOT null,
registration_date date not null
);