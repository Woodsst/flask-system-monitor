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


request_id_numbers = set()


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
        self.writhe_data_thread = None
        self.interval = 1
        self.start_time = time.strftime('%a, %d %b %Y %H:%M:%S')

    def receive(self) -> typing.Optional[protocol.MessageType]:
        message = self.websocket.receive()
        logger.info(f'included in web socket - {message}')
        try:
            json_data = json.loads(message)
        except json.decoder.JSONDecodeError:
            self.websocket.send(json.dumps(protocol.Error.ERROR_DATA_TYPE))
            logger.info(f'{message}, Data type incorrect')
            return

        client_request = protocol.MessageBase.deserialize(json_data)
        return client_request

    def handle(self, request):
        if request.type == protocol.MessageType.HELLO:
            self.client_status = ClientStatus.AUTHORIZED
            self.websocket.send(str(protocol.Welcome()))

        elif self.client_status != ClientStatus.NOT_AUTHORIZED:
            if request.type == protocol.MessageType.UNSUBSCRIBE:
                request_id_numbers.discard(request.request_id)
                if len(request_id_numbers) == 0:
                    self.client_status = ClientStatus.UNSUBSCRIBED
                    self.websocket.send(str(protocol.Unsubscribed(request.request_id)))
                    logger.info(f'client unsubscribed {request.request_id}')

            elif request.type == protocol.MessageType.SUBSCRIBE and request.request_id not in request_id_numbers:
                if request.request_id in request_id_numbers:
                    self.client_status = ClientStatus.AUTHORIZED
                    self.websocket.send(json.dumps(protocol.Error.ERROR_REQUEST_ID_COLLISION))
                else:
                    self.interval = int(request.interval)
                    request_id_numbers.add(request.request_id)
                    self.client_status = ClientStatus.SUBSCRIBED
                    self.websocket.send(str(protocol.Subscribed(request.request_id)))
                    logger.info(f'client subscribe {request.request_id}')
                    self.event_thread = threading.Thread(target=self.event, args=(request,))
                    self.event_thread.start()
                    self.writhe_data_thread = threading.Thread(target=self.write_response_data, args=(request,), daemon=True)
                    self.writhe_data_thread.start()
            elif request.type == protocol.MessageType.WORK_TIME:
                self.websocket.send(str(protocol.WorkTime(self.start_time, time.strftime('%d %b %Y %H:%M:%S'))))
        else:
            self.websocket.send(json.dumps(protocol.Error.ERROR_DATA_TYPE))

    def event(self, request):
        while self.client_status == ClientStatus.SUBSCRIBED and request.request_id in request_id_numbers:
            self.websocket.send(RequestHandler.handler(request))
            time.sleep(self.interval)

    def write_response_data(self, request):
        data_name = request.data[0].lower()

        csv_data = open(f'{data_name}_load.csv', 'w')
        csv_data.write(f'Request Id;Time;{data_name}\n')
        csv_data.write(f'{request.request_id};{time.strftime("%d %b %H:%M:%S")};tracking start\n')

        while self.client_status == ClientStatus.SUBSCRIBED and request.request_id in request_id_numbers:
            Data_load = json.loads(RequestHandler.handler(request))
            csv_data.write(f'{request.request_id};{time.strftime("%H:%M:%S")};{Data_load["payload"][data_name]}\n')
            time.sleep(self.interval)

        csv_data.write(f'{request.request_id};{time.strftime("%d %b %H:%M:%S")};tracking end\n')
