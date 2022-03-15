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
from authorization import *
from monitoring import write_client_data

logger = logging.getLogger(__file__)


class ClientStatus(enum.Enum):
    NOT_AUTHORIZED = 'NOT AUTHORIZED'
    AUTHORIZED = 'AUTHORIZED'
    SUBSCRIBED = 'SUBSCRIBED'
    UNSUBSCRIBED = 'UNSUBSCRIBED'


request_id_numbers = set()


def handler_data_for_protocol(data):
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
        logger.debug(f'included in web socket - {message}')
        try:
            json_data = json.loads(message)
        except TypeError:
            logger.debug('incorrect request from client or client disconnect')
            return
        except json.decoder.JSONDecodeError:
            self.websocket.send(json.dumps(protocol.Error.ERROR_DATA_TYPE))
            logger.debug(f'{message}, Data type incorrect')
            return
        client_request = protocol.MessageBase.deserialize(json_data)
        return client_request

    def message_hello(self):
        self.client_status = ClientStatus.AUTHORIZED
        self.websocket.send(str(protocol.Welcome()))

    def message_unsubscribe(self, request):
        request_id_numbers.discard(request.request_id)
        if len(request_id_numbers) == 0:
            self.client_status = ClientStatus.UNSUBSCRIBED
            self.websocket.send(str(protocol.Unsubscribed(request.request_id)))
            logger.info(f'client unsubscribed {request.request_id}')

    def message_subscribe(self, request):
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

    def message_client_data(self, request):
        username = id_verification(request.client_id)
        if username:
            if len(request.client_data) > 0:
                write_client_data(data=request.client_data, username=username)
                self.websocket.send(str(protocol.DataReturn(data=request.client_data)))
            else:
                self.websocket.send(str(protocol.Error.ERROR_DATA_SIZE))
                logger.info(f'client - {username} incorrect data size')

    def message_client_registration(self, request):
        username = request.username
        password = request.password
        if user_verification(username):
            client_id = authorization(username, password)
            if client_id:
                self.websocket.send(str(protocol.ExistClient(client_id)))
                logger.info(f'client: {username}, authorization')
            else:
                self.websocket.send(str(protocol.Error.ERROR_USERNAME_PASSWORD_INCORRECT))
        else:
            if username is None:
                self.websocket.send(str(protocol.Error.ERROR_USERNAME_PASSWORD_INCORRECT))
                return
            client_id = add_client(username, password)
            self.websocket.send(str(protocol.AddClient(username, client_id)))
            logger.info(f'client: {username}, registered')

    def handle(self, request):
        if request.type == protocol.MessageType.HELLO:
            self.message_hello()

        elif self.client_status != ClientStatus.NOT_AUTHORIZED:
            if request.type == protocol.MessageType.CLIENT_DATA:
                self.message_client_data(request)

            elif request.type == protocol.MessageType.REGISTRATION_CLIENT:
                self.message_client_registration(request)

            elif request.type == protocol.MessageType.UNSUBSCRIBE:
                self.message_unsubscribe(request)

            elif request.type == protocol.MessageType.SUBSCRIBE and request.request_id not in request_id_numbers:
                self.message_subscribe(request)

            elif request.type == protocol.MessageType.WORK_TIME:
                self.websocket.send(str(protocol.WorkTime(self.start_time, time.strftime('%d %b %Y %H:%M:%S'))))

        else:
            self.websocket.send(json.dumps(protocol.Error.ERROR_DATA_TYPE))

    def event(self, request):
        while self.client_status == ClientStatus.SUBSCRIBED and request.request_id in request_id_numbers:
            self.websocket.send(handler_data_for_protocol(request))
            time.sleep(self.interval)
