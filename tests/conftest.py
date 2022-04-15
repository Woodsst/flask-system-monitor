import psycopg
import pytest
from client import WebSocketTestApi, BaseHttpApi


@pytest.fixture(scope='function')
def ws_api():
    ws = WebSocketTestApi("localhost", 5000, "/echo")
    yield ws


@pytest.fixture(scope='session')
def api_client():
    httpapi = BaseHttpApi('localhost', 5000)
    yield httpapi


@pytest.fixture(scope='session')
def psql():
    conn = psycopg.connect(dbname='clients', user='wood', password='123', host="database", port=5432)
    yield conn
