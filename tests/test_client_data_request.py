import pytest
from psycopg import sql
from client_data import client_id, user, password, header, data


def test_client_data_request_202(api_client, psql):
    cur = psql.cursor()
    api_client.post(path='/client', json={'username': user, 'pass': password})
    response = api_client.post(f'/client/{client_id}', data=data,
                                 headers=header)
    assert response.status_code == 202
    response_json = response.json()
    assert isinstance(response_json, dict)
    assert len(response_json) == 4
    for value in response_json.values():
        assert isinstance(value, (int, float))
    cur.execute(sql.SQL("""SELECT * FROM {} WHERE time=1646650624""").format(sql.Identifier(user)))
    db_data = cur.fetchone()
    assert len(db_data) == 4
    assert db_data[0] == 25.9
    assert db_data[1] == 6172.0
    assert db_data[2] == 95888.0
    assert db_data[3] == 1646650624
    cur.execute("DELETE FROM clients WHERE username = %s ", params=(user,))
    cur.execute(sql.SQL("DROP TABLE {}").format(sql.Identifier(user)))
    psql.commit()


def test_client_data_request_405(api_client):
    api_client.post(path='/client', json={'username': user, 'pass': password})
    response = api_client.get(f'/client/{client_id}')
    assert response.status_code == 405
    response = api_client.put(f'/client/{client_id}')
    assert response.status_code == 405
    response = api_client.patch(f'/client/{client_id}')
    assert response.status_code == 405
    response = api_client.delete(f'/client/{client_id}')
    assert response.status_code == 405


def test_client_data_request_401(api_client, psql):
    api_client.post(path='/client', json={'username': user, 'pass': password})
    response = api_client.post(f'/client/{client_id}', data='',
                                 headers=header)
    assert response.status_code == 401
    response = api_client.post(f'/client/{client_id}', data=data,
                               headers={'Authorization': f'Basic afgjn123'})
    assert response.status_code == 401
    response = api_client.post(f'/client/{client_id}', data=data,
                               headers='')
    assert response.status_code == 401
    cur = psql.cursor()
    cur.execute("DELETE FROM clients WHERE username = %s ", params=(user,))
    cur.execute(sql.SQL("DROP TABLE {}").format(sql.Identifier(user)))
    psql.commit()

