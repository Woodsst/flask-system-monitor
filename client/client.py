import json

import requests
import websocket
from requests import Response

hello = json.dumps({"type": "HELLO"})
subscribe_cpu = json.dumps({"type": "SUBSCRIBE", "request_id": "1", "data": ["CPU"], "interval": "1"}, indent=4)
subscribe_mem = json.dumps({"type": "SUBSCRIBE", "request_id": "2", "data": ["MEM"], "interval": "1"}, indent=4)
subscribe_storage = json.dumps({"type": "SUBSCRIBE", "request_id": "3", "data": ["STORAGE"], "interval": "1"}, indent=4)
unsubscribe_cpu = json.dumps({"type": "UNSUBSCRIBE", "request_id": "1"}, indent=4)
unsubscribe_mem = json.dumps({"type": "UNSUBSCRIBE", "request_id": "2"}, indent=4)
unsubscribe_storage = json.dumps({"type": "UNSUBSCRIBE", "request_id": "3"}, indent=4)


class BaseHttpApi:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.base_url = f"http://{self.host}:{self.port}"

    def get(self, path, params=None) -> Response:
        url = self.base_url + path
        return requests.get(url, params=params)

    def post(self, path, data=None, json=None) -> Response:
        url = self.base_url + path
        return requests.post(url, data=data, json=json)

    def patch(self, path, data=None) -> Response:
        url = self.base_url + path
        return requests.patch(url, data=data)

    def delete(self, path) -> Response:
        url = self.base_url + path
        return requests.delete(url)

    def put(self, path, data=None, json=None) -> Response:
        url = self.base_url + path
        return requests.put(url, data=data, json=json)


class WebSocketTestClient:
    def __init__(self, host: str, port: int, path: str):
        self.host = host
        self.port = port
        self.path = path
        self.url = f'ws://{self.host}:{self.port}{self.path}'
        self.ws = websocket.WebSocket()
        self.ws.connect(self.url)

    def get(self, data: str):
        self.ws.send(data)

    def print_recv(self):
        print(self.ws.recv())

    def close(self):
        self.ws.close()


def test_subscribe_unsubscribe(data: str):
    data_dict = json.loads(data)
    timer = 0
    ws = WebSocketTestClient('localhost', 5000, '/echo')
    ws.get(hello)
    ws.get(data)
    while timer < 4:
        ws.print_recv()
        timer += 1
    if data_dict.get('request_id') == '1':
        ws.get(unsubscribe_cpu)
    elif data_dict.get('request_id') == '2':
        ws.get(unsubscribe_mem)
    elif data_dict.get('request_id') == '3':
        ws.get(unsubscribe_storage)
    ws.print_recv()


test_subscribe_unsubscribe(subscribe_cpu)
test_subscribe_unsubscribe(subscribe_mem)
test_subscribe_unsubscribe(subscribe_storage)
