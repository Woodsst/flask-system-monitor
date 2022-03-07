import base64
import os

import pytest

user = 'user'
password = 'password'
raw_directory = os.getcwd().split('/')
raw_directory.pop(-1)
server_directory = '/'.join(raw_directory) + '/server'
try:
    os.remove(f'{server_directory}/clients.csv')
    os.remove(f'{server_directory}/user_system_load.csv')
except FileNotFoundError:
    pass


def test_client_add_200(api_client):
    response = api_client.post(path='/client', json={'username': user, 'pass': password})
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['client_id'] == base64.b64encode(f'{user}:{password}'.encode()).decode()
    assert response_json['registration'] == user
    assert len(response_json) == 2
    with open(f'{server_directory}/clients.csv', 'r') as clients:
        assert clients.readlines()[-1].strip() == f'{user};{base64.b64encode(f"{user}:{password}".encode()).decode()}'
    os.remove(f'{server_directory}/clients.csv')
    os.remove(f'{server_directory}/user_system_load.csv')


def test_client_add_405(api_client):
    response = api_client.get(path='/client')
    assert response.status_code == 405
    response = api_client.put(path='/client', json={'username': user, 'pass': password})
    assert response.status_code == 405
    response = api_client.delete(path='/client')
    assert response.status_code == 405
    response = api_client.patch(path='/client')
    assert response.status_code == 405


def test_client_error_pass(api_client):
    response = api_client.post(path='/client', json={'username': user, 'pass': password})
    response = api_client.post(path='/client', json={'username': user, 'pass': 'asd'})
    response_json = response.json()
    assert response.status_code == 401
    assert response_json == {'Error': 'incorrect username or pass'}
    response = api_client.post(path='/client', json={'username': '', 'pass': password})
    assert response.status_code == 401
    assert response_json == {'Error': 'incorrect username or pass'}
    os.remove(f'{server_directory}/user_system_load.csv')
    os.remove(f'{server_directory}/clients.csv')
