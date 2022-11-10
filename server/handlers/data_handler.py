import json

from db import Psql


class ClientDataHandler:
    def __init__(self, database: Psql):
        self.db = database

    def write_client_data(self, data: dict, username: str):
        cpu = data.get("cpu_load")
        mem = data.get("mem")
        storage = data.get("storage")
        current_time = data.get("time")
        self.db.client_log(cpu, mem, storage, current_time, username)

    @staticmethod
    def to_json_for_client_data(data: dict) -> json:
        for key, _ in data.items():
            if key == "cpu_load":
                data[key] = float(data[key])
                continue
            data[key] = int(data[key])
        return json.dumps(data)
