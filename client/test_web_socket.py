import json
import time
import os

import pytest

hello = json.dumps({"type": "HELLO"})
welcome = '{"type": "WELCOME", "payload": {"welcome": "WELCOME"}}'
subscribe_cpu = json.dumps({"type": "SUBSCRIBE", "request_id": "1", "data": ["CPU"], "interval": "1"}, indent=4)
subscribe_cpu_interval_0 = json.dumps({"type": "SUBSCRIBE", "request_id": "1", "data": ["CPU"], "interval": "0"}, indent=4)
subscribe_mem = json.dumps({"type": "SUBSCRIBE", "request_id": "2", "data": ["MEM"], "interval": "1"}, indent=4)
subscribe_mem_interval_0 = json.dumps({"type": "SUBSCRIBE", "request_id": "2", "data": ["MEM"], "interval": "0.3"}, indent=4)
subscribe_storage = json.dumps({"type": "SUBSCRIBE", "request_id": "3", "data": ["STORAGE"], "interval": "1"}, indent=4)
subscribe_storage_interval_0 = json.dumps({"type": "SUBSCRIBE", "request_id": "3", "data": ["STORAGE"], "interval": "0.3"}, indent=4)
unsubscribe_cpu = json.dumps({"type": "UNSUBSCRIBE", "request_id": "1"}, indent=4)
unsubscribe_mem = json.dumps({"type": "UNSUBSCRIBE", "request_id": "2"}, indent=4)
unsubscribe_storage = json.dumps({"type": "UNSUBSCRIBE", "request_id": "3"}, indent=4)
unsubscribe_cpu_mem_storage = json.dumps({"type": "UNSUBSCRIBE", "request_id": "123"}, indent=4)
work_time = json.dumps({"type": "WORK_TIME"})
subscribe_cpu_mem_storage = json.dumps({"type": "SUBSCRIBE", "request_id": "123", "data": ["CPU", "MEM", "STORAGE"], "interval": "1"}, indent=4)


def test_hello(ws_api):
    ws_api.get(hello)
    assert ws_api.recv() == '{"type": "WELCOME", "payload": {"welcome": "WELCOME"}}'


def test_subscribe_unsubscribe_cpu(ws_api):
    ws_api.get(hello)
    ws_api.get(subscribe_cpu)
    assert ws_api.recv() == welcome
    assert ws_api.recv() == '{"type": "SUBSCRIBED", "payload": {"request_id": "1"}}'
    response_js = json.loads(ws_api.recv())
    assert response_js['type'] == 'EVENT'
    assert isinstance(response_js['payload']['cpu'], float)
    ws_api.get(unsubscribe_cpu)
    assert ws_api.recv() == '{"type": "UNSUBSCRIBED", "payload": {"request_id": "1"}}'


def test_subscribe_unsubscribe_mem(ws_api):
    ws_api.get(hello)
    ws_api.get(subscribe_mem)
    assert ws_api.recv() == welcome
    assert ws_api.recv() == '{"type": "SUBSCRIBED", "payload": {"request_id": "2"}}'
    response_js = json.loads(ws_api.recv())
    assert response_js['type'] == 'EVENT'
    assert isinstance(response_js['payload']['mem'], dict)
    assert len(response_js['payload']['mem']) == 11
    for value in response_js['payload']['mem'].values():
        assert isinstance(value, (int, float))
    ws_api.get(unsubscribe_mem)
    assert ws_api.recv() == '{"type": "UNSUBSCRIBED", "payload": {"request_id": "2"}}'


def test_subscribe_unsubscribe_storage(ws_api):
    ws_api.get(hello)
    ws_api.get(subscribe_storage)
    assert ws_api.recv() == welcome
    assert ws_api.recv() == '{"type": "SUBSCRIBED", "payload": {"request_id": "3"}}'
    response_js = json.loads(ws_api.recv())
    assert response_js['type'] == 'EVENT'
    assert isinstance(response_js['payload']['storage'], dict)
    assert len(response_js['payload']['storage']) == 4
    for value in response_js['payload']['storage'].values():
        assert isinstance(value, (int, float))
    ws_api.get(unsubscribe_storage)
    assert ws_api.recv() == '{"type": "UNSUBSCRIBED", "payload": {"request_id": "3"}}'


def test_subscribe_unsubscribe_cpu_mem_storage(ws_api):
    ws_api.get(hello)
    ws_api.get(subscribe_cpu_mem_storage)
    assert ws_api.recv() == welcome
    assert ws_api.recv() == '{"type": "SUBSCRIBED", "payload": {"request_id": "123"}}'
    response_js = json.loads(ws_api.recv())
    assert response_js['type'] == 'EVENT'
    assert len(response_js['payload']) == 4
    assert isinstance(response_js['payload']['cpu'], float)
    assert isinstance(response_js['payload']['storage'], dict)
    assert isinstance(response_js['payload']['mem'], dict)
    for value in response_js['payload']['mem'].values():
        isinstance(value, (int, float))
    for value in response_js['payload']['storage'].values():
        isinstance(value, (int, float))
    ws_api.get(unsubscribe_cpu_mem_storage)
    assert ws_api.recv() == '{"type": "UNSUBSCRIBED", "payload": {"request_id": "123"}}'


def test_work_time(ws_api):
    ws_api.get(hello)
    ws_api.get(work_time)
    assert ws_api.recv() == welcome
    response_js = json.loads(ws_api.recv())
    assert response_js['type'] == 'WORK_TIME'
    assert len(response_js['payload']) == 2
    assert isinstance(response_js['payload']['start_work'], str)
    assert isinstance(response_js['payload']['actual_time'], str)


def test_write_response_data_cpu(ws_api):
    ws_api.get(hello)
    ws_api.get(subscribe_cpu_interval_0)
    assert ws_api.recv() == welcome
    time.sleep(0.9)
    path = os.getcwd()
    path = path.removesuffix('client')
    path += 'server'
    csv_data = open(f'{path}/cpu_load.csv', 'r')
    file_string = csv_data.readlines()
    assert file_string[0] == 'Request Id;Time;cpu\n'
    assert file_string[1].split(';')[-1] == 'tracking start\n'
    assert file_string[-1].split(';')[-1] == 'tracking end\n'
    ws_api.get(unsubscribe_cpu)
    os.remove(path=f'{path}/cpu_load.csv')


def test_write_response_data_mem(ws_api):
    ws_api.get(hello)
    ws_api.get(subscribe_mem_interval_0)
    assert ws_api.recv() == welcome
    time.sleep(0.5)
    path = os.getcwd()
    path = path.removesuffix('client')
    path += 'server'
    csv_data = open(f'{path}/mem_load.csv', 'r')
    file_string = csv_data.readlines()
    assert file_string[0] == 'Request Id;Time;mem\n'
    assert file_string[1].split(';')[-1] == 'tracking start\n'
    assert file_string[-1].split(';')[-1] == 'tracking end\n'
    ws_api.get(unsubscribe_mem)
    os.remove(path=f'{path}/mem_load.csv')


def test_write_response_data_storage(ws_api):
    ws_api.get(hello)
    ws_api.get(subscribe_storage_interval_0)
    assert ws_api.recv() == welcome
    time.sleep(0.5)
    path = os.getcwd()
    path = path.removesuffix('client')
    path += 'server'
    csv_data = open(f'{path}/storage_load.csv', 'r')
    file_string = csv_data.readlines()
    assert file_string[0] == 'Request Id;Time;storage\n'
    assert file_string[1].split(';')[-1] == 'tracking start\n'
    assert file_string[-1].split(';')[-1] == 'tracking end\n'
    ws_api.get(unsubscribe_mem)
    os.remove(path=f'{path}/storage_load.csv')

