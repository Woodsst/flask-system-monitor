# flask-system-monitor
Hello! this is server for data storage.
This server work by Flask RESTful system for collection data.
Server support two data transfer type - http and web socket.
Clients information storage in PostgreSQL.

## Requariments
* python 3.9
* websocket-client
* future
* requests
* psutil
* Flask
* Flask-Sockets
* pytest-cov
* psycopg
* psycopg-binary
* pyYAML
* pydantic
* flake8
* black
* all requariments in server/requariments.txt

## PostgreSQL
* version 12+
* cofiguration for db connect in root - config_for_github.yml file

# Server work examples
for fast test - use docker and gui client for this server
## Docker
* docker compose file in root
if use docker-compose - data base deployed with server
docker-compose.yml for stable version in container
for him:
```
path_in_repository/flask_system_monitor$ docker-compose up
```
for tests docker-compose-dev.yml
for him: 
```
path_in_repository/flask_system_monitor$ docker-compose -f docker-compose-dev.yml -p test
```
this container create database, deployed server and use all tests for server
## Test GUI client
https://github.com/Woodsst/system-monitor-client
## Server stores received client system data
### Examples server work:
we a registration on server: 
```
url: localhost:5000/client
{
  "username": "wood", "password": "123"
}
```
and return 
```
{
  "client_id": "d29vZDoxMjM=",
  "registration": "wood"
}
```
client_id this is your unique code for transfer system data
and now we have two variants: 
first - transfer data in http requests 
second - transfer data in websocket

### Transfer data in http requests
server take your data from POST method and write in database
for example:
```
url: http://localhost:5000/client/wood
Headers: Authorization: d29vZDoxMjM=
Data: {
  "cpu_load": 25.9,
  "mem": 6172,
  "storage": 95888,
  "time": 1646650624
}
```
that request write data in database

and if we want, we send request for response about log write work time
```
localhost:5000/client/wood/time
```
server returned json with start and end work time log write
```
{
  "end": 1646650624,
  "start": 1646650624
}
```

if we need create log slice for specific time
```
url: localhost:5000/client/wood/time/report?start=1651155333&end=1651155431
```
and server return:
```
{
  "payload": [
    {
      "cpu": 18,
      "mem": 8513,
      "storage": 81720,
      "unix_time": 1651155333
    },
    {
      "cpu": 20,
      "mem": 8490,
      "storage": 81707,
      "unix_time": 1651155387
    },
    {
      "cpu": 20.5,
      "mem": 8516,
      "storage": 81708,
      "unix_time": 1651155431
    }
  ]
}
```
all log data is recorded in the database, each client separately

## Web Socket transfer data
For web socket url: ws//:localhost:5000/echo
there is a protocol for web socket operation
protocol works with serialise/deserialise json
for connect need small message
```
{
  "type": "HELLO"
}
```
if server return
```
{
  "type": "WELCOME",
  "payload": {
    "welcome": "WELCOME"
  }
}
```
we a ready for transfer data
format for transfer this is json 
```
{
  "type": "CLIENT_DATA",
  "data": {
    "cpu": 18,
    "mem": 8513,
    "storage": 81720,
    "unix_time": 1651155333
  },
  "interval": 1,
  "client_id": "d29vZDoxMjM="
}
```
## Server stores data about itself
### For example:
```
url: localhost:5000/monitor/cpu/load
```
return 
```
{
  "load": 7.0
}
```
Each request will return the current information about the server system.
Server collection data for cpu, memory and storage
```
localhost:5000/monitor/cpu/load
{"load":3.6}
localhost:5000/monitor/memory/info?units=MB
{
  "active": 1965,
  "available": 17820,
  "buffers": 284,
  "cached": 5148,
  "free": 12969,
  "inactive": 8335,
  "percent": 25.8,
  "shared": 203,
  "slab": 431,
  "total": 24002,
  "used": 5600
}
localhost:5000/monitor/storage/info?units=MB
{
  "free": 130349,
  "percent": 38.5,
  "total": 223357,
  "units": "MB",
  "used": 81594
}
```
Server also writes a log of its status in csv file - server_system_load.csv, in server directory
