import pytest
from client import WebSocketTestClient, BaseHttpApi


@pytest.fixture
def ws_api():
    ws = WebSocketTestClient("localhost", 5000, "/echo")
    return ws


@pytest.fixture
def api_client():
    httpapi = BaseHttpApi('localhost', 5000)
    return httpapi

