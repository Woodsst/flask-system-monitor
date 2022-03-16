import pytest
from client import WebSocketTestClient, BaseHttpApi


@pytest.fixture(scope='function')
def ws_api():
    ws = WebSocketTestClient("localhost", 5000, "/echo")
    print('create Websocket connect')
    yield ws


@pytest.fixture(scope='session')
def api_client():
    httpapi = BaseHttpApi('localhost', 5000)
    print('create HTTP connect')
    yield httpapi

