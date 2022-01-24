import enum
import json
import logging
import threading
import time
import typing

import cpu_monitor
import memory_monitor
import protocol
import storage_monitor
from datatype import DataType

logger = logging.getLogger(__file__)


class ClientStatus(enum.Enum):
    NOT_AUTHORIZED = 'NOT AUTHORIZED'
    AUTHORIZED = 'AUTHORIZED'
    SUBSCRIBED = 'SUBSCRIBED'
    UNSUBSCRIBED = 'UNSUBSCRIBED'


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


class WebSocketMessageHandler:
    def __init__(self, web_socket):
        self.websocket = web_socket
        self.client_status = ClientStatus.NOT_AUTHORIZED
        self.event_thread = None

    def receive(self) -> typing.Optional[protocol.MessageType]:
        message = self.websocket.receive()
        logger.info(f'included in web socket - {message}')
        try:
            json_data = json.loads(message)
        except json.decoder.JSONDecodeError:
            self.websocket.send(protocol.Error.ERROR_DATA_TYPE_MESSAGE)
            logger.info(f'{message}, Data type incorrect')
            return

        client_request = protocol.MessageBase.deserialize(json_data)
        return client_request

    def handle(self, request):
        if request.type == protocol.MessageType.HELLO:
            self.client_status = ClientStatus.AUTHORIZED
            self.websocket.send(str(protocol.Welcome()))

        if self.client_status != ClientStatus.NOT_AUTHORIZED:

            if request.type == protocol.MessageType.UNSUBSCRIBE:
                self.client_status = ClientStatus.UNSUBSCRIBED
                self.websocket.send(str(protocol.Unsubscribed(request.request_id)))
                logger.info(f'client unsubscribed {request.request_id}')

            elif request.type == protocol.MessageType.SUBSCRIBE:
                self.client_status = ClientStatus.SUBSCRIBED
                self.websocket.send(str(protocol.Subscribed(request.request_id)))
                logger.info(f'client subscribe {request.request_id}')
                self.event_thread = threading.Thread(target=self.event, args=(request,))
                self.event_thread.start()
        else:
            self.websocket.send('{"type": "ERROR", "reason": "not authorized"}')

    def event(self, request):
        while self.client_status == ClientStatus.SUBSCRIBED:
            self.websocket.send(RequestHandler.handler(request))
            time.sleep(1)
