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


def write_client_data(data, username):  # data = {cpu: 123, mem: 123, storage: 123}
    cpu = data.get('cpu_load', '')
    mem = data.get('mem', '')
    storage = data.get('storage', '')
    current_time = data.get('time')
    with open(f'{username}_system_load.csv', 'a') as file:
        file.write(f'{current_time};{cpu};{mem};{storage}\n')


def client_log_request(username, start_log, end_log):
    with open(f'{username}_system_load.csv', 'r') as file:
        file_string = file.readlines()
        start_index = 0
        end_index = 0
        payload = []
        for sting in file_string:
            if start_log in sting:
                start_index = file_string.index(sting)
            if end_log in sting:
                end_index = file_string.index(sting)
        for sting in file_string[start_index:end_index]:
            payload.append(sting.strip())
        return {
            "payload": payload
        }
        