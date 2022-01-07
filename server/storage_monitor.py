import psutil


def storage_info(Kb = False, Mb = False, Gb = False, Tb = False) -> dict:
    storage = psutil.disk_usage('/')
    storage_dict = {
        'total': storage[0],
        'percent': storage[3],
        'used': storage[1],
        'free': storage[2],
    }
    for memory in storage_dict:
        if memory != 'percent':
            if Kb is True:
                storage_dict[memory] = storage_dict[memory] // 1024
            if Mb is True:
                storage_dict[memory] = storage_dict[memory] // (1024 ** 2)
            if Gb is True:
                storage_dict[memory] = storage_dict[memory] // (1024 ** 3)
            if Tb is True:
                storage_dict[memory] = storage_dict[memory] / (1024 ** 4)
    return storage_dict
