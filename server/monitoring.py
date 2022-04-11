import time
import os

from cpu_monitor import cpu_load
from protocol import WorkTime
from memory_monitor import memory_info
from datatype import DataType
from storage_monitor import storage_info
from authorization import db
from typing import List

path = os.path.dirname(__file__)


def service_time(start_time: int) -> str:
    return str(WorkTime(start_time, time.strftime('%d %b %Y %H:%M:%S')))


def write_server_system_load():
    with open(f'{path}/server_system_load.csv', 'a', encoding='utf-8') as csv:
        csv.write('time;cpu load;memory load;storage\n')
        while True:
            csv.write(
                f'{time.strftime("%d %b %H:%M:%S")};'
                f'{cpu_load(1)};'
                f'{memory_info(DataType.MEGABYTE)["used"]};'
                f'{storage_info(DataType.MEGABYTE)["used"]}\n')
            csv.flush()


def write_client_data(data: dict, username: str):
    cpu = data.get('cpu_load')
    mem = data.get('mem')
    storage = data.get('storage')
    current_time = data.get('time')
    db.client_log(cpu, mem, storage, current_time, username)


def client_log_request(username, start: int, end: int) -> dict:
    if (start and end) > 0:
        raw_payload = db.client_log_request(username, start, end)
    else:
        raw_payload = db.client_full_log(username)
    return payload_formatting(raw_payload)


def payload_formatting(data: List[tuple]) -> dict:
    payload = []
    for cpu, mem, storage, unix_time in data:
        payload.append(dict(cpu=cpu, mem=mem, storage=storage, unix_time=unix_time))
    return {
        'payload': payload
    }


def time_write_log(username: str) -> dict:
    raw_time = db.log_write_time(username)
    return {
            "start": raw_time[0],
            "end": raw_time[1]
        }
