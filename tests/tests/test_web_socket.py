import json

from ..data_for_tests.client import WebSocketResponse as ws_respose
from ..data_for_tests.client_data import (
    WSRequestsForServerMonitoring as ws_request,
)


def test_hello(ws_api):
    assert ws_api.recv() == ws_respose.WELCOME


def test_subscribe_unsubscribe_cpu(ws_api):
    ws_api.get(ws_request.SUBSCRIBE_CPU)
    assert ws_api.recv() == ws_respose.SUBSCRIBE_CPU
    response_js = json.loads(ws_api.recv())
    assert response_js["type"] == "EVENT"
    assert isinstance(response_js["payload"]["cpu"], float)
    ws_api.get(ws_request.UNSUBSCRIBE_CPU)
    assert ws_api.recv() == ws_respose.UNSUBSCRIBED_CPU


def test_subscribe_unsubscribe_mem(ws_api):
    ws_api.get(ws_request.SUBSCRIBE_MEM)
    assert ws_api.recv() == ws_respose.SUBSCRIBE_MEM
    response_js = json.loads(ws_api.recv())
    assert response_js["type"] == "EVENT"
    assert isinstance(response_js["payload"]["mem"], dict)
    assert len(response_js["payload"]["mem"]) == 11
    for value in response_js["payload"]["mem"].values():
        assert isinstance(value, (int, float))
    ws_api.get(ws_request.UNSUBSCRIBE_MEM)
    assert ws_api.recv() == ws_respose.UNSUBSCRIBED_MEM


def test_subscribe_unsubscribe_storage(ws_api):
    ws_api.get(ws_request.SUBSCRIBE_STORAGE)
    assert ws_api.recv() == ws_respose.SUBSCRIBE_STORAGE
    response_js = json.loads(ws_api.recv())
    assert response_js["type"] == "EVENT"
    assert isinstance(response_js["payload"]["storage"], dict)
    assert len(response_js["payload"]["storage"]) == 4
    for value in response_js["payload"]["storage"].values():
        assert isinstance(value, (int, float))
    ws_api.get(ws_request.UNSUBSCRIBE_STORAGE)
    assert ws_api.recv() == ws_respose.UNSUBSCRIBED_STORAGE


def test_subscribe_unsubscribe_cpu_mem_storage(ws_api):
    ws_api.get(ws_request.SUBSCRIBE_CPU_MEM_STORAGE)
    assert ws_api.recv() == ws_respose.SUBSCRIBE_CPU_MEM_STORAGE
    response_js = json.loads(ws_api.recv())
    assert response_js["type"] == "EVENT"
    assert len(response_js["payload"]) == 4
    assert isinstance(response_js["payload"]["cpu"], float)
    assert isinstance(response_js["payload"]["storage"], dict)
    assert isinstance(response_js["payload"]["mem"], dict)
    for value in response_js["payload"]["mem"].values():
        isinstance(value, (int, float))
    for value in response_js["payload"]["storage"].values():
        isinstance(value, (int, float))
    ws_api.get(ws_request.UNSUBSCRIBE_CPU_MEM_STORAGE)
    assert ws_api.recv() == ws_respose.UNSUBSCRIBED_CPU_MEM_STORAGE


def test_work_time(ws_api):
    ws_api.get(ws_request.WORK_TIME)
    response_js = json.loads(ws_api.recv())
    assert response_js["type"] == "WORK_TIME"
    assert len(response_js["payload"]) == 2
    assert isinstance(response_js["payload"]["start_work"], str)
    assert isinstance(response_js["payload"]["actual_time"], str)


def test_error_data_type(ws_api):
    ws_api.get(ws_request.INCORRECT_DATA_TYPE)
    request = ws_api.recv()
    assert isinstance(request, str)
    assert len(request) > 0
    assert request == ws_respose.ERROR_DATA_TYPE


def test_json_decode_error(ws_api):
    ws_api.get(ws_request.INCORRECT_JSON)
    request = ws_api.recv()
    assert isinstance(request, str)
    assert len(request) > 0
    assert request == ws_respose.ERROR_DATA_TYPE


def test_data_type_error_in_handle():
    from ..data_for_tests.client import WebSocketTestApi

    ws_api = WebSocketTestApi("localhost", 5000, "/echo")
    ws_api.get(ws_request.WELCOME)
    request = ws_api.recv()
    assert isinstance(request, str)
    assert len(request) > 0
    assert request == ws_respose.ERROR_DATA_TYPE
