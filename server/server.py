import logging
import threading
import time

from logger_config import logger_config

from flask import Flask, make_response, request, Response, jsonify
from flask_sockets import Sockets, Rule

from cpu_monitor import cpu_load, cpu_core_info, cpu_frequencies
from datatype import DataType
from memory_monitor import memory_info
from message_handler import WebSocketMessageHandler
from storage_monitor import storage_info
from monitoring import write_client_data, client_log_request, write_server_system_load, service_time
from authorization import hash_authorization, user_exist, authorization, error_authorization, add_client, \
    id_verification

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
    return {
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
    username = id_verification(client_id)
    if username:
        if hash_authorization(client_hash):
            data = request.form
            if len(data) > 0:
                write_client_data(data, username)
                return jsonify(request.form), 202
            logger.info(f'client - {username} incorrect data size')
            return jsonify(f'client - {username} incorrect data size'), 401
        else:
            logger.info(f'client - {username} incorrect hash')
            return jsonify(f'client - {username} incorrect hash'), 401
    else:
        return error_authorization(request)


@app.route('/client', methods=['POST'])
def client_registration() -> Response or dict:
    username = request.get_json()['username']
    password = request.get_json()['pass']
    if user_exist(username):
        client_id = authorization(username=username, password=password)
        if client_id:
            logger.info(f'client: {username}, authorization')
            return {
                'client_id': client_id,
            }
        else:
            return error_authorization(request)
    else:
        if username is None:
            return error_authorization(request)
        client_id = add_client(username, password)
        logger.info(f'client: {username}, registered')
        return {
            'registration': username,
            'client_id': client_id
        }


@app.route('/client/<client_id>/time', methods=["GET"])
def client_log_time_work(client_id):
    with open('Clients.csv', 'r') as file:
        for string in file.readlines():
            string.strip()
            username, client_id_in_file = string.split(';')
            if client_id == client_id_in_file:
                if user_exist(username):
                    with open(f'{username}_system_load.csv', 'r') as file:
                        count = file.readlines()
                        time_start_write = count[1].split(';')[0]
                        last_time = count[-1].split(';')[0]
                        response_js = {
                            "start": time_start_write,
                            "end": last_time
                        }
                        return response_js, 200
                else:
                    return error_authorization(request)


@app.route('/client/<client_id>/time/report', methods=["GET"])
def split_client_log(client_id):
    with open('Clients.csv', 'r') as file:
        for string in file.readlines():
            string.strip()
            username, client_id_in_file = string.split(';')
            if client_id == client_id_in_file:
                if user_exist(username):
                    start = request.args.get('start')
                    end = request.args.get('end')
                    payload = client_log_request(username, start, end)
                    return payload, 200
                else:
                    return error_authorization(request)


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
