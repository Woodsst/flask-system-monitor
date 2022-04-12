import logging
import threading
import time
from typing import Union

from flask import Flask, make_response, request, Response, jsonify
from flask_sockets import Sockets, Rule

from authorization import user_verification, authorization, error_authorization, add_client, \
    id_verification, to_json_for_client_data
from cpu_monitor import cpu_load, cpu_core_info, cpu_frequencies
from datatype import DataType
from logger_config import logger_config
from memory_monitor import memory_info
from message_handler import WebSocketMessageHandler
from monitoring import write_client_data, client_log_request, write_server_system_load, service_time, time_write_log
from storage_monitor import storage_info

app = Flask(__name__)
sockets = Sockets(app)

logger = logging.getLogger(__file__)


@app.route("/")
def welcome() -> str:
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


@app.route('/client/<client_id>', methods=['POST'])
def route_for_client(client_id) -> Union[tuple[Response, int], tuple[any, int]]:
    try:
        client = request.headers.get('Authorization').split(' ')[-1]
        if client != client_id:
            return jsonify(''), 401
    except AttributeError:
        return jsonify(''), 401
    username = id_verification(client)
    if username:
        data = request.form.to_dict()
        if len(data) > 0:
            write_client_data(data, username)
            return to_json_for_client_data(data), 202
        logger.info('client - %s incorrect data size', username)
        return jsonify(''), 401
    logger.info('client - %s incorrect client_id', username)
    return jsonify(''), 401


@app.route('/client', methods=['POST'])
def client_registration() -> Response or dict:
    username = request.get_json()['username']
    password = request.get_json()['pass']
    if not username[0].isalpha():
        return jsonify({'error': 'unsupportable username'}), 400
    if user_verification(username):
        client_id = authorization(username=username, password=password)
        if client_id:
            logger.info('client: %s, authorization', username)
            return jsonify({'client_id': client_id})
        return error_authorization(request), 401
    if username is None or len(username) == 0:
        return error_authorization(request), 401
    client_id = add_client(username, password)
    logger.info('client: %s, registered', username)
    return jsonify({
        'registration': username,
        'client_id': client_id
    })


@app.route('/client/<client_id>/time', methods=["GET"])
def client_log_time_work(client_id: str) -> Response:
    username = id_verification(client_id)
    if username and user_verification(username):
        response_js = time_write_log(username)
        if response_js.get('error'):
            return response_js
        return response_js, 200
    else:
        return error_authorization(request), 401


@app.route('/client/<client_id>/time/report', methods=["GET"])
def split_client_log(client_id: str) -> Response:
    username = id_verification(client_id)
    if username and user_verification(username):
        start = request.args.get('start')
        end = request.args.get('end')
        if (len(end) and len(start)) == 0:
            start = 0
            end = 0
        try:
            payload = client_log_request(username, int(start), int(end))
        except ValueError:
            return jsonify({'error': 'value error'}), 400
        return payload, 200
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
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
