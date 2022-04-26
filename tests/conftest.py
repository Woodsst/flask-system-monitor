import time

import pytest
import requests as requests

from client import WebSocketTestApi, BaseHttpApi
from client_data import user
from server_command import terminate_server, server_run
from config import Settings
from client_data import WSRequestsForServerMonitoring as ws_request

config = Settings()


@pytest.fixture(scope='session')
def start_server_for_tests(api_client):
    config.config_for_tests()
    server_run()
    timeout = 0.01
    while True:
        time.sleep(timeout)
        try:
            api_client.get('/api')
        except requests.exceptions.ConnectionError:
            timeout += 0.01
            if timeout > 0.2:
                return
            continue
        break
    yield
    config.reset_default_config()
    terminate_server()


@pytest.fixture(scope='session')
def ws_api(hello: bool = True):
    ws = WebSocketTestApi("localhost", 5000, "/echo")
    if hello is True:
        ws.get(ws_request.HELLO)
    yield ws


@pytest.fixture(scope='session')
def api_client():
    httpapi = BaseHttpApi('localhost', 5000)
    yield httpapi


@pytest.fixture(scope='session')
def psql():
    from db import PostgresClient
    conn = PostgresClient(dbname=config.db_name, user=config.db_username,
                           password=config.db_password, host=config.db_host, port=config.db_port)
    try:
        yield conn
    finally:
        conn.delete_username(user)
        conn.drop_table(user)
