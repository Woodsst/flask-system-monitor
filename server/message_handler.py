import protocol
import storage_monitor
import cpu_monitor
import memory_monitor
from datatype import DataType


class RequestHandler:

    @staticmethod
    def handler(data):
        message = data
        if 'CPU' in message.data:
            cpu = cpu_monitor.cpu_load(0.1)
        else:
            cpu = None
        if 'MEM' in message.data:
            mem = memory_monitor.memory_info(DataType.Megabyte)
        else:
            mem = None
        if 'STORAGE' in message.data:
            storage = storage_monitor.storage_info(DataType.Gigabyte)
        else:
            storage = None
        return str(protocol.Event(cpu, mem, storage, message.request_id))
