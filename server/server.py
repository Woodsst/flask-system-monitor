import logging
import threading
import time

import logger_config

from flask import Flask, make_response, request, Response, jsonify
from flask_sockets import Sockets, Rule

from cpu_monitor import cpu_load, cpu_core_info, cpu_frequencies
from datatype import DataType
from memory_monitor import memory_info
from message_handler import WebSocketMessageHandler
from storage_monitor import storage_info
from monitoring import service_time, write_cpu_load
from authorization import authorization, user_exist, add_client, hash_authorization

app = Flask(__name__)
sockets = Sockets(app)

logger = logging.getLogger(__file__)


@app.route("/")
def welcome():
    return "<p>Welcome</p>"


@sockets.route('/echo', websocket=True)
def echo_socket(ws):
    handler = WebSocketMessageHandler(ws)
    while not ws.closed:
        client_request = handler.receive()
        if client_request is None:
            continue
        handler.handle(client_request)


@app.route('/api')
def api_info() -> dict:
    return {
        'name': 'system monitor',
        'version': '0.0.1',
    }


@app.route('/monitor/cpu/load')
def processor_load() -> dict:
    interval = request.args.get('interval', 0)
    return {
        'load': cpu_load(float(interval)),
    }


@app.route('/monitor/cpu/info')
def cpu_cores() -> dict:
    physical = cpu_core_info(logical=False)
    logical = cpu_core_info(logical=True)
    frequency = cpu_frequencies()
    return {
        "physical cores count": physical,
        "logical cores count": logical,
        'cores frequency': frequency
    }


@app.route('/monitor/memory/info')
def memory_all_info() -> Response or dict:
    raw_units = request.args.get('units', "GB")
    try:
        units = DataType(raw_units)
        print(units)
    except ValueError:
        return make_response("Bad units provided", 400)
    return memory_info(units)


@app.route('/monitor/memory/total')
def memory_total() -> Response or dict:
    raw_units = request.args.get('units', "GB")
    try:
        units = DataType(raw_units)
    except ValueError:
        return make_response("Bad units provided", 400)
    return {
        'total': memory_info(units)['total'],
        'units': units.value,
    }


@app.route('/monitor/storage/info')
def storage_all_info() -> Response or dict:
    raw_units = request.args.get('units', 'GB')
    try:
        units = DataType(raw_units)
    except ValueError:
        return make_response("Bad units provided", 400)
    return {
        "total": storage_info(units)['total'],
        'used': storage_info(units)['used'],
        'percent': storage_info(units)['percent'],
        'free': storage_info(units)['free'],
        "units": units.value,
    }


@app.route('/monitor/storage/total')
def storage_total() -> Response or dict:
    raw_units = request.args.get('units', 'GB')
    try:
        units = DataType(raw_units)
    except ValueError:
        return make_response("Bad units provided", 400)
    return{
        'total': storage_info(units)['total'],
        'used': storage_info(units)['used'],
        'units': units.value,
    }


@app.route('/start_time')
def start_time() -> Response or dict:
    return service_time(server_start)


@app.route(f'/client/<client_id>', methods=['POST'])
def route_for_client(client_id: int) -> Response:
    client_hash = request.headers.get('Authorization').removeprefix('Basic ')
    if hash_authorization(client_id, client_hash):
        data = request.form['cpu_load']
        with open(f'client_{client_id}_cpu_load.csv', 'a') as client_cpu:
            client_cpu.write(f'{data}\n')
            return jsonify(data), 202
    else:
        return jsonify(''), 401


@app.route('/client', methods=['POST'])
def client_registration() -> Response or dict:
    login = request.get_json()['login']
    password = request.get_json()['pass']
    if user_exist(login):
        client_id = authorization(user=login, password=password)
        if client_id:
            return {
               'client_id': client_id,
            }
        else:
            logger.info(f'{request.get_json()}, incorrect login or pass')
            return {
                'Error': 'incorrect login or pass'
            }
    else:
        client_id = add_client(login, password)
        return {
            'registration': login,
            'client_id': client_id
        }


if __name__ == "__main__":
    logger.info(f'server start')
    server_start = time.strftime('%a, %d %b %Y %H:%M:%S')
    thread_cpu_info = threading.Thread(target=write_cpu_load, daemon=True)
    thread_cpu_info.start()
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    sockets.url_map.add(Rule("/echo", endpoint=echo_socket, websocket=True))
    server.serve_forever()
