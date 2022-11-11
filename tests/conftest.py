import time

import pytest
import requests as requests

from tests.data_for_tests.client import WebSocketTestApi, BaseHttpApi
from tests.data_for_tests.client_data import user
from .server_command import terminate_server, server_run
from .config import Settings
from tests.data_for_tests.client_data import (
    WSRequestsForServerMonitoring as ws_request,
)
from .db import PostgresClient

config = Settings()


@pytest.fixture(scope="session")
def start_server_for_tests(api_client):
    server_run()
    timeout = 0.01
    while True:
        time.sleep(timeout)
        try:
            api_client.get("/api")
        except requests.exceptions.ConnectionError:
            timeout += 0.01
            if timeout > 0.2:
                return
            continue
        break
    yield
    terminate_server()


@pytest.fixture(scope="session")
def ws_api(hello: bool = True):
    ws = WebSocketTestApi(config.app.host,
                          config.app.port,
                          config.app.ws)
    if hello is True:
        ws.get(ws_request.HELLO)
    yield ws


@pytest.fixture(scope="session")
def api_client():
    httpapi = BaseHttpApi(config.app.host,
                          config.app.port,)
    yield httpapi


@pytest.fixture(scope="session")
def psql():
    conn = PostgresClient(
        dbname=config.storage.name,
        user=config.storage.username,
        password=config.storage.password,
        host=config.storage.host,
        port=config.storage.port,
    )
    try:
        yield conn
    finally:
        conn.delete_username(user)
        conn.drop_table(user)
