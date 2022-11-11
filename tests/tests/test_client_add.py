from ..data_for_tests.client_data import user, password, client_id


def test_client_add_200(api_client, psql):
    response = api_client.post(
        path="/client", json={"username": user, "pass": password}
    )
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["client_id"] == client_id
    assert response_json["registration"] == user
    assert len(response_json) == 2
    fetch = psql.select_username_uniq_id(user)
    assert fetch[0] == user
    assert fetch[1] == client_id


def test_client_error_pass(api_client):
    api_client.post(path="/client", json={"username": user, "pass": password})
    response = api_client.post(
        path="/client", json={"username": user, "pass": "asd"}
    )
    response_json = response.json()
    assert response.status_code == 401
    assert response_json == {"error": "authorization error"}
    response = api_client.post(
        path="/client", json={"username": "", "pass": password}
    )
    assert response.status_code == 401
    assert response_json == {"error": "authorization error"}


def test_client_username_validation(api_client):
    response = api_client.post(
        path="/client", json={"username": "123", "pass": password}
    )
    assert response.status_code == 401
    assert response.json() == {"error": "unsupportable username"}
    response = api_client.post(
        path="/client", json={"username": "", "pass": password}
    )
    assert response.status_code == 401
    assert response.json() == {"error": "unsupportable username"}
