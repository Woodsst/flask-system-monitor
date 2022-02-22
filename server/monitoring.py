import time
import os

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
            csv.write(f'{time.strftime("%d %b %H:%M:%S")};{cpu_load(1)};{memory_info(DataType.Megabyte)["used"]};{storage_info(DataType.Megabyte)["used"]}\n')
            csv.flush()


def write_client_data(data, username, data_name):
    try:
        parent_dir = os.getcwd()
        path = os.path.join(parent_dir, username)
        os.mkdir(path)
    except FileExistsError:
        pass
    with open(f'{os.getcwd()}/{username}/{username}_{data_name}.csv', 'a') as file:
        file.write(f'{data}\n')
