import psycopg
import pytest
from psycopg import sql

from client import WebSocketTestApi, BaseHttpApi
from client_data import user


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
    conn = psycopg.connect(dbname='clients', user='wood', password='123', host="database", port=5432)
    try:
        yield conn
    finally:
        conn.cursor().execute("DELETE FROM clients WHERE username = %s ", params=(user,))
        conn.cursor().execute(sql.SQL("DROP TABLE {}").format(sql.Identifier(user)))
        conn.commit()
