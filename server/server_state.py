import os
import time

from monitoring_utilities.cpu_monitor import cpu_load
from monitoring_utilities.datatype import DataType
from monitoring_utilities.memory_monitor import memory_info
from handlers.protocol import WorkTime
from monitoring_utilities.storage_monitor import storage_info

path = os.path.dirname(__file__)


def service_time(start_time: int) -> str:
    return str(WorkTime(start_time, time.strftime("%d %b %Y %H:%M:%S")))


def write_server_system_load():
    with open(f"{path}/server_system_load.csv", "a", encoding="utf-8") as csv:
        csv.write("time;cpu load;memory load;storage\n")
        while True:
            csv.write(
                f'{time.strftime("%d %b %H:%M:%S")};'
                f"{cpu_load(1)};"
                f'{memory_info(DataType.MEGABYTE)["used"]};'
                f'{storage_info(DataType.MEGABYTE)["used"]}\n'
            )
            csv.flush()
