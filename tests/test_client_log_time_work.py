import base64

import pytest

import os

user = 'user'
password = 'password'
raw_directory = os.getcwd().split('/')
raw_directory.pop(-1)
server_directory = '/'.join(raw_directory) + '/server'
try:
    os.remove(f'{server_directory}/user_system_load.csv')
except FileNotFoundError:
    pass
client_id = base64.b64encode(f'{user}:{password}'.encode()).decode()
data = {"cpu_load": 25.9, "mem": 6172, "storage": 95888, "time": 1646650624}
data_2 = {"cpu_load": 20.9, "mem": 6272, "storage": 95838, "time": 1646650625}
header = {'Authorization': f'Basic {client_id}'}


def test_client_log_time_work(api_client, psql):
    api_client.post(path='/client', json={'username': user, 'pass': password})
    api_client.post(f'/client/{client_id}', data=data, headers=header)
    api_client.post(f'/client/{client_id}', data=data_2, headers=header)
    response = api_client.get(f'/client/{client_id}/time')
    response_js = response.json()
    assert response_js['start'] == '1646650624'
    assert response_js['end'] == '1646650625'
    with open(f'{server_directory}/{user}_system_load.csv', 'r') as file:
        count = file.readlines()
        time_start_write = count[1].split(';')[0]
        last_time = count[-1].split(';')[0]
        assert time_start_write == '1646650624'
        assert last_time == '1646650625'
    os.remove(f'{server_directory}/user_system_load.csv')
    cur = psql.cursor()
    cur.execute("DELETE FROM clients WHERE username = %s ", params=(user,))
    psql.commit()
