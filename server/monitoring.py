import time

from cpu_monitor import cpu_load
from protocol import WorkTime
from memory_monitor import memory_info
from datatype import DataType
from storage_monitor import storage_info


def service_time(start_time: int) -> str:
    return str(WorkTime(start_time, time.strftime('%d %b %Y %H:%M:%S')))


def write_server_system_load():
    with open('server_system_load.csv', 'a', encoding='utf-8') as csv:
        csv.write('time;cpu load;memory load;storage\n')
        while True:
            csv.write(
                f'{time.strftime("%d %b %H:%M:%S")};'
                f'{cpu_load(1)};'
                f'{memory_info(DataType.MEGABYTE)["used"]};'
                f'{storage_info(DataType.MEGABYTE)["used"]}\n')
            csv.flush()


def write_client_data(data: dict, username: str):
    cpu = data.get('cpu_load', '')
    mem = data.get('mem', '')
    storage = data.get('storage', '')
    current_time = data.get('time')
    with open(f'{username}_system_load.csv', 'a', encoding='utf-8') as file:
        file.write(f'{current_time};{cpu};{mem};{storage}\n')


def client_log_request(username, start_log: int, end_log: int) -> dict:
    with open(f'{username}_system_load.csv', 'r', encoding='utf-8') as file:
        payload = []
        file_string = file.readlines()
        if len(file_string) <= 1:
            return
        if start_log == 0 and end_log == 0:
            for string in file_string:
                payload.append(string.strip())
            return {
                "payload": payload
            }
        for string in file_string[1:]:
            strng = int(string.strip().split(';')[0])
            if start_log <= strng <= end_log:
                payload.append(string.strip())
        return {
            "payload": payload
        }
        