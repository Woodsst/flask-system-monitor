import base64

import pytest

from psycopg import sql

user = 'test_user'
password = 'password'
client_id = base64.b64encode(f'{user}:{password}'.encode()).decode()
data = {"cpu_load": 25.9, "mem": 6172, "storage": 95888, "time": 1646650624}
data_2 = {"cpu_load": 20.9, "mem": 6272, "storage": 95838, "time": 1646650625}
data_3 = {"cpu_load": 20.9, "mem": 6272, "storage": 95838, "time": 1646650626}
header = {'Authorization': f'Basic {client_id}'}


def test_split_log(api_client, psql):
    api_client.post(path='/client', json={'username': user, 'pass': password})
    api_client.post(f'/client/{client_id}', data=data, headers=header)
    api_client.post(f'/client/{client_id}', data=data_2, headers=header)
    api_client.post(f'/client/{client_id}', data=data_3, headers=header)
    response = api_client.get(path=f'/client/{client_id}/time/report?start={1646650624}&end={1646650626}')
    response_json = response.json()
    assert response.status_code == 200
    assert isinstance(response_json['payload'], list)
    assert len(response_json) == 1
    assert len(response_json['payload']) == 3
    cur = psql.cursor()
    cur.execute("DELETE FROM clients WHERE username = %s ", params=(user,))
    cur.execute(sql.SQL("DROP TABLE {}").format(sql.Identifier(user)))
    psql.commit()
