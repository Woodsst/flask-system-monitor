import enum

import protocol
import storage_monitor
import cpu_monitor
import memory_monitor
from datatype import DataType


class RequestHandler:

    @staticmethod
    def handler(data):
        message = protocol.MessageBase.deserialize(data)
        if message.type == protocol.MessageType.HELLO:
            return str(protocol.Welcome())
        elif message.type == protocol.MessageType.SUBSCRIBE:
            pass

