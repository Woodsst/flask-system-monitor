import time

from cpu_monitor import cpu_load
from protocol import WorkTime
from memory_monitor import memory_info
from datatype import DataType


def service_time(start_time):
    return str(WorkTime(start_time, time.strftime('%d %b %Y %H:%M:%S')))


def write_cpu_load():
    with open(f'all_time_cpu_load.csv', 'a') as csv:
        csv.write(f'time;cpu load;memory load\n')
        while True:
            csv.write(f'{time.strftime("%d %b %H:%M:%S")};{cpu_load(1)};{memory_info(DataType.Megabyte)["used"]}\n')
            csv.flush()

