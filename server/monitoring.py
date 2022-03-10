import time

from cpu_monitor import cpu_load
from protocol import WorkTime
from memory_monitor import memory_info
from datatype import DataType
from storage_monitor import storage_info


def service_time(start_time):
    return str(WorkTime(start_time, time.strftime('%d %b %Y %H:%M:%S')))


def write_server_system_load():
    with open(f'server_system_load.csv', 'a') as csv:
        csv.write(f'time;cpu load;memory load;storage\n')
        while True:
            csv.write(
                f'{time.strftime("%d %b %H:%M:%S")};{cpu_load(1)};{memory_info(DataType.Megabyte)["used"]};{storage_info(DataType.Megabyte)["used"]}\n')
            csv.flush()


def write_client_data(data, username):
    cpu = data.get('cpu_load', '')
    mem = data.get('mem', '')
    storage = data.get('storage', '')
    current_time = data.get('time')
    with open(f'{username}_system_load.csv', 'a') as file:
        file.write(f'{current_time};{cpu};{mem};{storage}\n')


def client_log_request(username, start_log, end_log):
    with open(f'{username}_system_load.csv', 'r') as file:
        file_string = file.readlines()
        payload = []
        for string in file_string:
            if start_log >= string[0] <= end_log:
                payload.append(string.strip())
        return {
            "payload": payload
        }
        