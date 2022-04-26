import enum
import json


class MessageType(enum.Enum):
    HELLO = 'HELLO'
    WELCOME = 'WELCOME'
    SUBSCRIBE = 'SUBSCRIBE'
    SUBSCRIBED = 'SUBSCRIBED'
    UNSUBSCRIBE = 'UNSUBSCRIBE'
    UNSUBSCRIBED = 'UNSUBSCRIBED'
    EVENT = 'EVENT'
    ERROR = 'ERROR'
    WORK_TIME = 'WORK_TIME'
    CLIENT_DATA = 'CLIENT_DATA'
    DATA_RETURN = 'DATA_RETURN'
    EXIST_CLIENT = 'EXIST_CLIENT'


class MessageBase:
    type: MessageType

    @classmethod
    def deserialize(cls, data):
        raw_message_type = data.get('type')
        if raw_message_type is None:
            return
        message_type = MessageType(raw_message_type)
        message_cls = message_cls_map.get(message_type)
        message_data = data.get('data')
        request_id = data.get('request_id')
        interval = data.get('interval')
        username = data.get('username')
        password = data.get('password')
        client_id = data.get('client_id')
        if username is not None:
            return message_cls(username=username, password=password)
        if message_data is not None and isinstance(message_data, (int, float, dict)):
            return message_cls(message_data, interval, client_id)
        if message_data is not None and len(message_data) != 0:
            return message_cls(message_data, request_id, interval)
        if request_id is not None:
            return message_cls(request_id=request_id)
        return message_cls

    def __str__(self):
        return str(self.as_json())

    def as_json(self):
        json_data = {
            'type': self.type.value,
            'payload': self.__dict__
        }
        return json.dumps(json_data)


class Hello(MessageBase):
    type: MessageType = MessageType.HELLO

    def __init__(self, client_message: str):
        self.msg = client_message


class Welcome(MessageBase):
    type: MessageType = MessageType.WELCOME

    def __init__(self):
        self.welcome = 'WELCOME'


class Subscribe(MessageBase):
    type: MessageType = MessageType.SUBSCRIBE

    def __init__(self, data: list, request_id: int, interval: float):
        self.data = data
        self.request_id = request_id
        self.interval = interval


class Subscribed(MessageBase):
    type: MessageType = MessageType.SUBSCRIBED

    def __init__(self, request_id: int):
        self.request_id = request_id


class Unsubscribe(MessageBase):
    type: MessageType = MessageType.UNSUBSCRIBE

    def __init__(self, request_id: int):
        self.request_id = request_id


class Unsubscribed(MessageBase):
    type: MessageType = MessageType.UNSUBSCRIBED

    def __init__(self, request_id: int):
        self.request_id = request_id


class WorkTime(MessageBase):
    type: MessageType = MessageType.WORK_TIME

    def __init__(self, start_time: int, actual_time: int):
        self.start_work = start_time
        self.actual_time = actual_time


class Event(MessageBase):
    type: MessageType = MessageType.EVENT

    def __init__(self, cpu: float = None, mem: dict = None,
                 storage: dict = None, request_id: int = None):
        self.request = request_id
        self.cpu = cpu
        self.mem = mem
        self.storage = storage


class ClientData(MessageBase):
    type: MessageType = MessageType.CLIENT_DATA

    def __init__(self, client_data: dict, interval: int, client_id: str):
        self.client_data = client_data
        self.interval = interval
        self.client_id = client_id


class DataReturn(MessageBase):
    type: MessageType = MessageType.DATA_RETURN

    def __init__(self, data: dict):
        self.data = data


class ExistClient(MessageBase):
    type: MessageType = MessageType.EXIST_CLIENT

    def __init__(self, client_id: str):
        self.client_id = client_id


class Error(MessageBase):
    type: MessageType = MessageType.ERROR

    ERROR_DATA_TYPE = {
        "type": "ERROR", "reason": "Data type incorrect, please use json"
    }
    ERROR_REQUEST_ID_COLLISION = {
        "type": "ERROR", "reason": "request id collision"
    }
    ERROR_USERNAME_PASSWORD_INCORRECT = {
        "type": "ERROR", "reason": "incorrect username or password"
    }
    ERROR_DATA_SIZE = {
        "type": "ERROR", "reason": "incorrect data size"
    }


message_cls_map = {
    MessageType.HELLO: Hello,
    MessageType.WELCOME: Welcome,
    MessageType.SUBSCRIBE: Subscribe,
    MessageType.SUBSCRIBED: Subscribed,
    MessageType.UNSUBSCRIBE: Unsubscribe,
    MessageType.UNSUBSCRIBED: Unsubscribed,
    MessageType.EVENT: Event,
    MessageType.ERROR: Error,
    MessageType.WORK_TIME: WorkTime,
    MessageType.CLIENT_DATA: ClientData,
    MessageType.DATA_RETURN: DataReturn,
    MessageType.EXIST_CLIENT: ExistClient,

}
