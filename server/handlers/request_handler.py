from typing import List

from db import Psql


class RequestHandler:
    def __init__(self, database: Psql) -> None:
        self.db = database

    def client_log_request(self, username, start: int, end: int) -> dict:
        if (start and end) > 0:
            raw_payload = self.db.client_log_request(username, start, end)
        else:
            raw_payload = self.db.client_full_log(username)
        return self.payload_formatting(raw_payload)

    @staticmethod
    def payload_formatting(data: List[tuple]) -> dict:
        payload = []
        for cpu, mem, storage, unix_time in data:
            payload.append(dict(cpu=cpu, mem=mem, storage=storage, unix_time=unix_time))
        return {
            'payload': payload
        }

    def time_write_log(self, username: str) -> dict:
        raw_time = self.db.log_write_time(username)
        if (raw_time[0] and raw_time[1]) is None:
            return {"error": "log is empty"}
        return {
            "start": raw_time[0],
            "end": raw_time[1]
        }
