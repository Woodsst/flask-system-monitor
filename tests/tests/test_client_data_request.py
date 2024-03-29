from ..data_for_tests.client_data import user, password, header, data


def test_client_data_request_202(api_client, psql):
    api_client.post(path="/client", json={"username": user, "pass": password})
    response = api_client.post(f"/client/{user}", data=data, headers=header)
    assert response.status_code == 202
    response_json = response.json()
    assert isinstance(response_json, dict)
    assert len(response_json) == 4
    for value in response_json.values():
        assert isinstance(value, (int, float))
    db_data = psql.select_raw_data_for_time(user, "1646650624")
    assert len(db_data) == 4
    assert db_data[0] == 25.9
    assert db_data[1] == 6172.0
    assert db_data[2] == 95888.0
    assert db_data[3] == 1646650624


def test_client_data_request_405(api_client):
    api_client.post(path="/client", json={"username": user, "pass": password})
    response = api_client.get(f"/client/{user}")
    assert response.status_code == 405
    response = api_client.put(f"/client/{user}")
    assert response.status_code == 405
    response = api_client.patch(f"/client/{user}")
    assert response.status_code == 405
    response = api_client.delete(f"/client/{user}")
    assert response.status_code == 405


def test_client_data_request_401(api_client):
    api_client.post(path="/client", json={"username": user, "pass": password})
    response = api_client.post(f"/client/{user}", data="", headers=header)
    assert response.status_code == 400
    response = api_client.post(
        f"/client/{user}",
        headers={"Authorization": "Basic afgjn123"},
        data=data,
    )
    assert response.status_code == 401
    response = api_client.post(f"/client/{user}", data=data, headers="")
    assert response.status_code == 401
