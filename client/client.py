from requests import Response
import requests


class BaseHttpApi:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.base_url = f"http://{self.host}:{self.port}"

    def get(self, path, params=None) -> Response:
        url = self.base_url + path
        return requests.get(url, params=params)

    def post(self, path, data=None, json=None) -> Response:
        url = self.base_url + path
        return requests.post(url, data=data, json=json)

    def patch(self, path, data=None) -> Response:
        url = self.base_url + path
        return requests.patch(url, data=data)

    def delete(self, path) -> Response:
        url = self.base_url + path
        return requests.delete(url)

    def put(self, path, data=None, json=None) -> Response:
        url = self.base_url + path
        return requests.put(url, data=data, json=json)


base_api = BaseHttpApi('localhost', 5000)

response = base_api.get("/api")
response1 = base_api.get("/monitor/storage/total?units=MB")
# print(response.status_code)
print(response1.status_code)
# print(response.json())
print(response1.json())
