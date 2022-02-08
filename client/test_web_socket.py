import json
import pytest
from client import WebSocketTestClient

hello = json.dumps({"type": "HELLO"})
subscribe_cpu = json.dumps({"type": "SUBSCRIBE", "request_id": "1", "data": ["CPU"], "interval": "1"}, indent=4)
subscribe_mem = json.dumps({"type": "SUBSCRIBE", "request_id": "2", "data": ["MEM"], "interval": "1"}, indent=4)
subscribe_storage = json.dumps({"type": "SUBSCRIBE", "request_id": "3", "data": ["STORAGE"], "interval": "1"}, indent=4)
unsubscribe_cpu = json.dumps({"type": "UNSUBSCRIBE", "request_id": "1"}, indent=4)
unsubscribe_mem = json.dumps({"type": "UNSUBSCRIBE", "request_id": "2"}, indent=4)
unsubscribe_storage = json.dumps({"type": "UNSUBSCRIBE", "request_id": "3"}, indent=4)


def test_hello():
    ws_api = WebSocketTestClient("localhost", 5000, "/echo")
    ws_api.get(hello)
    assert ws_api.recv() == '{"type": "WELCOME", "payload": {"welcome": "WELCOME"}}'


def test_subscribe_unsubscribe_cpu():
    ws_api = WebSocketTestClient('localhost', 5000, '/echo')
    ws_api.get(hello)
    ws_api.get(subscribe_cpu)
    assert ws_api.recv() == '{"type": "WELCOME", "payload": {"welcome": "WELCOME"}}'
    assert ws_api.recv() == '{"type": "SUBSCRIBED", "payload": {"request_id": "1"}}'
    response_js = json.loads(ws_api.recv())
    assert response_js['type'] == 'EVENT'
    assert isinstance(response_js['payload']['cpu'], float)
    ws_api.get(unsubscribe_cpu)
    assert ws_api.recv() == '{"type": "UNSUBSCRIBED", "payload": {"request_id": "1"}}'


def test_subscribe_unsubscribe_mem():
    ws_api = WebSocketTestClient('localhost', 5000, '/echo')
    ws_api.get(hello)
    ws_api.get(subscribe_mem)
    assert ws_api.recv() == '{"type": "WELCOME", "payload": {"welcome": "WELCOME"}}'
    assert ws_api.recv() == '{"type": "SUBSCRIBED", "payload": {"request_id": "2"}}'
    response_js = json.loads(ws_api.recv())
    assert response_js['type'] == 'EVENT'
    assert isinstance(response_js['payload']['mem'], dict)
    ws_api.get(unsubscribe_mem)
    assert ws_api.recv() == '{"type": "UNSUBSCRIBED", "payload": {"request_id": "2"}}'


def test_subscribe_unsubscribe_storage():
    ws_api = WebSocketTestClient('localhost', 5000, '/echo')
    ws_api.get(hello)
    ws_api.get(subscribe_storage)
    assert ws_api.recv() == '{"type": "WELCOME", "payload": {"welcome": "WELCOME"}}'
    assert ws_api.recv() == '{"type": "SUBSCRIBED", "payload": {"request_id": "3"}}'
    response_js = json.loads(ws_api.recv())
    assert response_js['type'] == 'EVENT'
    assert isinstance(response_js['payload']['storage'], dict)
    ws_api.get(unsubscribe_storage)
    assert ws_api.recv() == '{"type": "UNSUBSCRIBED", "payload": {"request_id": "3"}}'
