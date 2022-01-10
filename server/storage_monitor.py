import psutil
from datatype import DataType


def storage_info(arg: str) -> dict:
    storage = psutil.disk_usage('/')
    storage_dict = {
        'total': storage[0],
        'percent': storage[3],
        'used': storage[1],
        'free': storage[2],
    }
    for memory in storage_dict:
        if memory != 'percent':
            if arg == DataType.Kilobyte.value:
                storage_dict[memory] = storage_dict[memory] // 1024
            if arg == DataType.Megabyte.value:
                storage_dict[memory] = storage_dict[memory] // (1024 ** 2)
            if arg == DataType.Gigabyte.value:
                storage_dict[memory] = storage_dict[memory] // (1024 ** 3)
            if arg == DataType.Terabyte.value:
                storage_dict[memory] = storage_dict[memory] / (1024 ** 4)
    return storage_dict
