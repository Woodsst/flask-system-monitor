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


class WebSocketTestApi:
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
    DATA_RETURN_FOR_DATA_1 = '{"type": "DATA_RETURN", "payload": {"data": {"cpu_load": 25.9, "mem": 6172, "storage": 95888, "time": 1646650624}}}'
    ERROR_DATA_SIZE = "{'type': 'ERROR', 'reason': 'incorrect data size'}"
    ERROR_DATA_TYPE = '{"type": "ERROR", "reason": "Data type incorrect, please use json"}'
