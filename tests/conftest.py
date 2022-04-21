import time

import psycopg
import pytest
import requests as requests
from psycopg import sql

from client import WebSocketTestApi, BaseHttpApi
from client_data import user
from server_command import terminate_server, server_run
from config import Settings

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


@pytest.fixture(scope='function')
def ws_api():
    ws = WebSocketTestApi("localhost", 5000, "/echo")
    yield ws


@pytest.fixture(scope='session')
def api_client():
    httpapi = BaseHttpApi('localhost', 5000)
    yield httpapi


@pytest.fixture(scope='function')
def psql():
    conn = psycopg.connect(dbname=config.db_name, user=config.db_username,
                           password=config.db_password, host=config.db_host, port=config.db_port)
    try:
        yield conn
    finally:
        conn.cursor().execute("DELETE FROM clients WHERE username = %s ", params=(user,))
        conn.cursor().execute(sql.SQL("DROP TABLE {}").format(sql.Identifier(user)))
        conn.commit()
