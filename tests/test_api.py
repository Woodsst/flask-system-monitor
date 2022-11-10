def test_api_200(api_client, start_server_for_tests):
    response = api_client.get("/api")
    assert response.status_code == 200, f"{response.status_code}"
    response_json = response.json()
    assert response_json["name"] == "system monitor"
    assert response_json["version"] == "0.0.1"


def test_api_405(api_client):
    response = api_client.post("/api")
    assert response.status_code == 405, f"{response.status_code}"
    response = api_client.put("/api")
    assert response.status_code == 405, f"{response.status_code}"
    response = api_client.patch("/api")
    assert response.status_code == 405, f"{response.status_code}"
    response = api_client.delete("/api")
    assert response.status_code == 405, f"{response.status_code}"


def test_welcome_200(api_client):
    response = api_client.get("/")
    assert response.status_code == 200
    assert response.content == b"<p>Welcome</p>"


def test_welcome_405(api_client):
    response = api_client.post("/")
    assert response.status_code == 405, f"{response.status_code}"
    response = api_client.put("/")
    assert response.status_code == 405, f"{response.status_code}"
    response = api_client.patch("/")
    assert response.status_code == 405, f"{response.status_code}"
    response = api_client.delete("/")
    assert response.status_code == 405, f"{response.status_code}"
