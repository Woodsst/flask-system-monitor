# flask-system-monitor
Hello! this is server for data storage.
This is a learning project, if you find problems, please let me know, thx.
This server work by Flask RESTful system for collection data.
Server support two data transfer type - http and web socket.
Clients information storage in PostgreSQL.

## Requariments
* python 3.9
* requarements.txt

## Docker
* docker compose file in root
if use docker-compose - data base deployed with server

## PostgreSQL
* version 12+

# Server work examples
## Server stores received client system data
### For example:
we a registration on server:
localhost:5000/client take JSON 
```
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
server take your data and write in data base
for example:
```
$ curl -H "Authorization: d29vZDoxMjM=" \
-d '{"cpu_load": 25.9, "mem": 6172, "storage": 95888, "time": 1646650624}' \
http://localhost:5000/client/d29vZDoxMjM=
```
return
```
{"cpu_load": 25.9, "mem": 6172, "storage": 95888, "time": 1646650624}
```
and if we want, we send request for response about  log write work time
```
$ curl localhost:5000/client/d29vZDoxMjM=/time
{"end":1646650624,"start":1646650624}
```
if we need create log slice for specific time
```
$ curl localhost:5000/client/d29vZDoxMjM=/time/report?start=1651155333&end=1651155431
{"payload":[{"cpu":18.0,"mem":8513.0,"storage":81720.0,"unix_time":1651155333},
{"cpu":20.0,"mem":8490.0,"storage":81707.0,"unix_time":1651155387},
{"cpu":20.5,"mem":8516.0,"storage":81708.0,"unix_time":1651155431}]}
```
all log data is recorded in the database, each client separately

## Server stores data about itself
### For example:
if you use bash in linux:
```
$ curl localhost:5000/monitor/cpu/load
{"load":7.0}
```
or your browser:

![Screenshot from 2022-04-28 11-42-54](https://user-images.githubusercontent.com/90110119/165713823-1a7d28f0-c1a8-4fb7-906f-0296b98c0789.png)

Each request will return the current information about the server system.
Server collection data for cpu, memory and storage
```
$ curl localhost:5000/monitor/cpu/load
{"load":3.6}
$ curl localhost:5000/monitor/memory/info?units=MB
{"active":1965,"available":17820,"buffers":284,"cached":5148,"free":12969,"inactive":8335,"percent":25.8,"shared":203,"slab":431,"total":24002,"used":5600}
$ curl localhost:5000/monitor/storage/info?units=MB
{"free":130349,"percent":38.5,"total":223357,"units":"MB","used":81594}
```
Server also writes a log of its status in csv file - server_system_load.csv, in server directory

## Test GUI client

https://github.com/Woodsst/system-monitor-client
