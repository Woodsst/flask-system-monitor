import psutil


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
            if arg == 'K':
                storage_dict[memory] = storage_dict[memory] // 1024
            if arg == 'M':
                storage_dict[memory] = storage_dict[memory] // (1024 ** 2)
            if arg == 'G':
                storage_dict[memory] = storage_dict[memory] // (1024 ** 3)
            if arg == 'T':
                storage_dict[memory] = storage_dict[memory] / (1024 ** 4)
    return storage_dict
