import base64
import os
from psycopg import sql

import pytest

user = 'test_user'
password = 'password'


def test_client_add_200(api_client, psql):
    cur = psql.cursor()
    response = api_client.post(path='/client', json={'username': user, 'pass': password})
    response_json = response.json()
    uniq_id = base64.b64encode(f'{user}:{password}'.encode()).decode()
    assert response.status_code == 200
    assert response_json['client_id'] == uniq_id
    assert response_json['registration'] == user
    assert len(response_json) == 2
    cur.execute('SELECT username, uniq_id FROM clients WHERE username = %s', params=(user,))
    fetch = cur.fetchone()
    assert fetch[0] == user
    assert fetch[1] == uniq_id
    cur.execute("DELETE FROM clients WHERE username = %s ", params=(user,))
    cur.execute(sql.SQL("DROP TABLE {}").format(sql.Identifier(user)))
    psql.commit()


def test_client_add_405(api_client):
    response = api_client.get(path='/client')
    assert response.status_code == 405
    response = api_client.put(path='/client', json={'username': user, 'pass': password})
    assert response.status_code == 405
    response = api_client.delete(path='/client')
    assert response.status_code == 405
    response = api_client.patch(path='/client')
    assert response.status_code == 405


def test_client_error_pass(api_client, psql):
    cur = psql.cursor()
    api_client.post(path='/client', json={'username': user, 'pass': password})
    response = api_client.post(path='/client', json={'username': user, 'pass': 'asd'})
    response_json = response.json()
    assert response.status_code == 401
    assert response_json == {'Error': 'incorrect username or pass'}
    response = api_client.post(path='/client', json={'username': '', 'pass': password})
    assert response.status_code == 401
    assert response_json == {'Error': 'incorrect username or pass'}
    cur.execute("DELETE FROM clients WHERE username = %s ", params=(user,))
    cur.execute(sql.SQL("DROP TABLE {}").format(sql.Identifier(user)))
    psql.commit()
