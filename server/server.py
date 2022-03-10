import json
import logging
import threading
import time
from typing import Union, Tuple

from flask import Flask, make_response, request, Response, jsonify
from flask_sockets import Sockets, Rule

from authorization import user_verification, authorization, error_authorization, add_client, \
    id_verification, to_json_for_client_data
from cpu_monitor import cpu_load, cpu_core_info, cpu_frequencies
from datatype import DataType
from logger_config import logger_config
from memory_monitor import memory_info
from message_handler import WebSocketMessageHandler
from monitoring import write_client_data, client_log_request, write_server_system_load, service_time
from storage_monitor import storage_info

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
    return {
        'total': storage_info(units)['total'],
        'used': storage_info(units)['used'],
        'units': units.value,
    }


@app.route('/start_time')
def start_time() -> Response or dict:
    return service_time(server_start)


@app.route(f'/client/<client_id>', methods=['POST'])
def route_for_client(client_id) -> Union[tuple[Response, int], tuple[any, int]]:
    try:
        request.headers.get('Authorization').split(' ')[-1]
    except AttributeError:
        return jsonify(''), 401
    client_hash = request.headers.get('Authorization').split(' ')[-1]
    username = id_verification(client_hash)
    if username:
        data = request.form.to_dict()
        if len(data) > 0:
            write_client_data(data, username)
            return to_json_for_client_data(data), 202
        logger.info(f'client - {username} incorrect data size')
        return jsonify(''), 401
    else:
        logger.info(f'client - {username} incorrect hash')
        return jsonify(''), 401


@app.route('/client', methods=['POST'])
def client_registration() -> Response or dict:
    username = request.get_json()['username']
    password = request.get_json()['pass']
    if user_verification(username):
        client_id = authorization(username=username, password=password)
        if client_id:
            logger.info(f'client: {username}, authorization')
            return {
                'client_id': client_id,
            }
        else:
            return error_authorization(request), 401
    else:
        if username is None or len(username) == 0:
            return error_authorization(request), 401
        client_id = add_client(username, password)
        logger.info(f'client: {username}, registered')
        return {
            'registration': username,
            'client_id': client_id
        }


@app.route('/client/<client_id>/time', methods=["GET"])
def client_log_time_work(client_id):
    username = id_verification(client_id)
    if username and user_verification(username):
        with open(f'{username}_system_load.csv', 'r') as file:
            count = file.readlines()
            if len(count) <= 1:
                return jsonify({
                    'error': 'log file is empty'
                }), 416
            time_start_write = count[1].split(';')[0]
            last_time = count[-1].split(';')[0]
            response_js = {
                "start": time_start_write,
                "end": last_time
            }
            return response_js, 200
    else:
        return error_authorization(request), 401


@app.route('/client/<client_id>/time/report', methods=["GET"])
def split_client_log(client_id):
    username = id_verification(client_id)
    if username and user_verification(username):
        start = request.args.get('start')
        end = request.args.get('end')
        payload = client_log_request(username, start, end)
        return payload, 200
    else:
        return error_authorization(request), 401


if __name__ == "__main__":
    logger_config()
    server_start = time.strftime('%a, %d %b %Y %H:%M:%S')
    thread_cpu_info = threading.Thread(target=write_server_system_load, daemon=True)
    thread_cpu_info.start()
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    sockets.url_map.add(Rule("/echo", endpoint=echo_socket, websocket=True))
    server.serve_forever()
