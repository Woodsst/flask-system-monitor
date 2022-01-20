import enum
import json

request_id = 0


class MessageType(enum.Enum):
    HELLO = 'HELLO'
    WELCOME = 'WELCOME'
    SUBSCRIBE = 'SUBSCRIBE'
    SUBSCRIBED = 'SUBSCRIBED'
    UNSUBSCRIBE = 'UNSUBSCRIBE'
    UNSUBSCRIBED = 'UNSUBSCRIBED'
    EVENT = 'EVENT'
    ERROR = 'ERROR'


class MessageBase:
    type: MessageType

    @classmethod
    def deserialize(cls, data):
        message = json.loads(data)
        raw_message_type = message.get('type')
        message_type = MessageType(raw_message_type)
        message_cls = message_cls_map.get(message_type)
        message_data = message.get('data')
        if len(message_data) != 0:
            return message_cls(message_data)
        return message_cls

    def __str__(self):
        return str(self.as_json())

    def as_json(self):
        json_data = {
            'type': self.type.value,
            'payload': self.__dict__
        }
        return json_data


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

    def __init__(self, data: list):
        self.data = data
        self.request = request_id


class Subscribed(MessageBase):
    type: MessageType = MessageType.SUBSCRIBED

    def __init__(self):
        global request_id
        self.request_id = request_id


class Unsubscribe(MessageBase):
    type: MessageType = MessageType.UNSUBSCRIBE

    def __init__(self):
        global request_id
        self.request_id = request_id
        request_id += 1


class Unsubscribed(MessageBase):
    type: MessageType = MessageType.UNSUBSCRIBED

    def __init__(self):
        self.request_id = request_id


class Event(MessageBase):
    type: MessageType = MessageType.EVENT

    def __init__(self, cpu, mem, storage):
        self.request = request_id
        self.cpu = cpu
        self.mem = mem
        self.storage = storage


class Error(MessageBase):
    type: MessageType = MessageType.ERROR

    def __init__(self, msg: str):
        self.msg = msg


message_cls_map = {
    MessageType.HELLO: Hello,
    MessageType.WELCOME: Welcome,
    MessageType.SUBSCRIBE: Subscribe,
    MessageType.SUBSCRIBED: Subscribed,
    MessageType.UNSUBSCRIBE: Unsubscribe,
    MessageType.UNSUBSCRIBED: Unsubscribed,
    MessageType.EVENT: Event,
    MessageType.ERROR: Error,

}
