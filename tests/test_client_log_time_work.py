import pytest

from psycopg import sql
from client_data import header, client_id, password, user, data, data_2


def test_client_log_time_work(api_client, psql):
    api_client.post(path='/client', json={'username': user, 'pass': password})
    api_client.post(f'/client/{client_id}', data=data, headers=header)
    api_client.post(f'/client/{client_id}', data=data_2, headers=header)
    response = api_client.get(f'/client/{client_id}/time')
    response_js = response.json()
    assert response_js['start'] == 1646650624
    assert response_js['end'] == 1646650625
    cur = psql.cursor()
    cur.execute("DELETE FROM clients WHERE username = %s ", params=(user,))
    cur.execute(sql.SQL("DROP TABLE {}").format(sql.Identifier(user)))
    psql.commit()
