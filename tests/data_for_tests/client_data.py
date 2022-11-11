import base64
import json

user = "test_user"
password = "password"
client_id = base64.b64encode(f"{user}:{password}".encode()).decode()

data = {"cpu_load": 25.9, "mem": 6172, "storage": 95888, "time": 1646650624}
data_2 = {"cpu_load": 20.9, "mem": 6272, "storage": 95838, "time": 1646650625}
data_3 = {"cpu_load": 20.9, "mem": 6272, "storage": 95838, "time": 1646650626}
header = {"Authorization": client_id}


class WSRequestsForServerMonitoring:
    HELLO = json.dumps({"type": "HELLO"})
    SUBSCRIBE_CPU = json.dumps(
        {
            "type": "SUBSCRIBE",
            "request_id": "1",
            "data": ["CPU"],
            "interval": "1",
        },
        indent=4,
    )
    SUBSCRIBE_CPU_INTERVAL_0 = json.dumps(
        {
            "type": "SUBSCRIBE",
            "request_id": "1",
            "data": ["CPU"],
            "interval": "0",
        },
        indent=4,
    )
    SUBSCRIBE_MEM = json.dumps(
        {
            "type": "SUBSCRIBE",
            "request_id": "2",
            "data": ["MEM"],
            "interval": "1",
        },
        indent=4,
    )
    SUBSCRIBE_MEM_INTERVAL_0 = json.dumps(
        {
            "type": "SUBSCRIBE",
            "request_id": "2",
            "data": ["MEM"],
            "interval": "0.3",
        },
        indent=4,
    )
    SUBSCRIBE_STORAGE = json.dumps(
        {
            "type": "SUBSCRIBE",
            "request_id": "3",
            "data": ["STORAGE"],
            "interval": "1",
        },
        indent=4,
    )
    SUBSCRIBE_STORAGE_INTERVAL_0 = json.dumps(
        {
            "type": "SUBSCRIBE",
            "request_id": "3",
            "data": ["STORAGE"],
            "interval": "0.3",
        },
        indent=4,
    )
    UNSUBSCRIBE_CPU = json.dumps(
        {"type": "UNSUBSCRIBE", "request_id": "1"}, indent=4
    )
    UNSUBSCRIBE_MEM = json.dumps(
        {"type": "UNSUBSCRIBE", "request_id": "2"}, indent=4
    )
    UNSUBSCRIBE_STORAGE = json.dumps(
        {"type": "UNSUBSCRIBE", "request_id": "3"}, indent=4
    )
    UNSUBSCRIBE_CPU_MEM_STORAGE = json.dumps(
        {"type": "UNSUBSCRIBE", "request_id": "123"}, indent=4
    )
    WORK_TIME = json.dumps({"type": "WORK_TIME"})
    SUBSCRIBE_CPU_MEM_STORAGE = json.dumps(
        {
            "type": "SUBSCRIBE",
            "request_id": "123",
            "data": ["CPU", "MEM", "STORAGE"],
            "interval": "1",
        },
        indent=4,
    )
    INCORRECT_DATA_TYPE = json.dumps({"incorrect": "request"})
    BAD_TYPE = json.dumps({"type": "bad"})
    INCORRECT_JSON = "incorrect json"
    WELCOME = json.dumps(
        {"type": "WELCOME", "payload": {"welcome": "WELCOME"}}
    )


class WSRequstsForClientSystemMonitoring:
    CLIENT_DATA = json.dumps(
        {
            "type": "CLIENT_DATA",
            "data": data,
            "interval": 1,
            "client_id": client_id,
        },
        indent=4,
    )
    EMPTY_CLIENT_DATA = json.dumps(
        {
            "type": "CLIENT_DATA",
            "data": {},
            "interval": 1,
            "client_id": client_id,
        },
        indent=4,
    )
