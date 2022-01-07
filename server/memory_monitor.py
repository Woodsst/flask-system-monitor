import psutil


def memory_info(Kb = False, Mb = False, Gb = False, Tb = False) -> dict:
    mem = psutil.virtual_memory()
    memory_dict = {
        'total': mem[0],
        'available': mem[1],
        'percent': mem[2],
        'used': mem[3],
        'free': mem[4],
        'active': mem[5],
        'inactive': mem[6],
        'buffers': mem[7],
        'cached': mem[8],
        'shared': mem[9],
        'slab': mem[10],
    }
    for memory in memory_dict:
        if memory != 'percent':
            if Kb is True:
                memory_dict[memory] = memory_dict[memory] / 1024
            if Mb is True:
                memory_dict[memory] = memory_dict[memory] / (1024 ** 2)
            if Gb is True:
                memory_dict[memory] = memory_dict[memory] / (1024 ** 3)
            if Tb is True:
                memory_dict[memory] = memory_dict[memory] / (1024 ** 4)
    return memory_dict
