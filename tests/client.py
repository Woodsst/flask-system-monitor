import json

import requests
import websocket
from requests import Response


class BaseHttpApi:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.base_url = f"http://{self.host}:{self.port}"

    def get(self, path, params=None) -> Response:
        url = self.base_url + path
        return requests.get(url, params=params)

    def post(self, path, data=None, json=None, **kwargs) -> Response:
        url = self.base_url + path
        return requests.post(url, data=data, json=json, **kwargs)

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

    def recv(self):
        return self.ws.recv()

    def close(self):
        self.ws.close()


class WebSocketRequests:
    HELLO = json.dumps({"type": "HELLO"})
    SUBSCRIBE_CPU = json.dumps({"type": "SUBSCRIBE", "request_id": "1", "data": ["CPU"], "interval": "1"}, indent=4)
    SUBSCRIBE_CPU_INTERVAL_0 = json.dumps({"type": "SUBSCRIBE", "request_id": "1", "data": ["CPU"], "interval": "0"},
                                          indent=4)
    SUBSCRIBE_MEM = json.dumps({"type": "SUBSCRIBE", "request_id": "2", "data": ["MEM"], "interval": "1"}, indent=4)
    SUBSCRIBE_MEM_INTERVAL_0 = json.dumps({"type": "SUBSCRIBE", "request_id": "2", "data": ["MEM"], "interval": "0.3"},
                                          indent=4)
    SUBSCRIBE_STORAGE = json.dumps({"type": "SUBSCRIBE", "request_id": "3", "data": ["STORAGE"], "interval": "1"},
                                   indent=4)
    SUBSCRIBE_STORAGE_INTERVAL_0 = json.dumps(
        {"type": "SUBSCRIBE", "request_id": "3", "data": ["STORAGE"], "interval": "0.3"}, indent=4)
    UNSUBSCRIBE_CPU = json.dumps({"type": "UNSUBSCRIBE", "request_id": "1"}, indent=4)
    UNSUBSCRIBE_MEM = json.dumps({"type": "UNSUBSCRIBE", "request_id": "2"}, indent=4)
    UNSUBSCRIBE_STORAGE = json.dumps({"type": "UNSUBSCRIBE", "request_id": "3"}, indent=4)
    UNSUBSCRIBE_CPU_MEM_STORAGE = json.dumps({"type": "UNSUBSCRIBE", "request_id": "123"}, indent=4)
    WORK_TIME = json.dumps({"type": "WORK_TIME"})
    SUBSCRIBE_CPU_MEM_STORAGE = json.dumps(
        {"type": "SUBSCRIBE", "request_id": "123", "data": ["CPU", "MEM", "STORAGE"], "interval": "1"}, indent=4)


class WebSocketResponse:
    WELCOME = '{"type": "WELCOME", "payload": {"welcome": "WELCOME"}}'
    SUBSCRIBE_CPU = '{"type": "SUBSCRIBED", "payload": {"request_id": "1"}}'
    UNSUBSCRIBED_CPU = '{"type": "UNSUBSCRIBED", "payload": {"request_id": "1"}}'
    SUBSCRIBE_MEM = '{"type": "SUBSCRIBED", "payload": {"request_id": "2"}}'
    UNSUBSCRIBED_MEM = '{"type": "UNSUBSCRIBED", "payload": {"request_id": "2"}}'
    SUBSCRIBE_STORAGE = '{"type": "SUBSCRIBED", "payload": {"request_id": "3"}}'
    UNSUBSCRIBED_STORAGE = '{"type": "UNSUBSCRIBED", "payload": {"request_id": "3"}}'
    SUBSCRIBE_CPU_MEM_STORAGE = '{"type": "SUBSCRIBED", "payload": {"request_id": "123"}}'
    UNSUBSCRIBED_CPU_MEM_STORAGE = '{"type": "UNSUBSCRIBED", "payload": {"request_id": "123"}}'
