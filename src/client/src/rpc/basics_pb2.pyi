from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BuyRequest(_message.Message):
    __slots__ = ("stock", "quantity", "id")
    STOCK_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    stock: str
    quantity: int
    id: int
    def __init__(self, stock: _Optional[str] = ..., quantity: _Optional[int] = ..., id: _Optional[int] = ...) -> None: ...

class TransactionSummary(_message.Message):
    __slots__ = ("cost",)
    COST_FIELD_NUMBER: _ClassVar[int]
    cost: int
    def __init__(self, cost: _Optional[int] = ...) -> None: ...

class HelloRequest(_message.Message):
    __slots__ = ("date", "hello")
    DATE_FIELD_NUMBER: _ClassVar[int]
    HELLO_FIELD_NUMBER: _ClassVar[int]
    date: int
    hello: str
    def __init__(self, date: _Optional[int] = ..., hello: _Optional[str] = ...) -> None: ...

class HelloReply(_message.Message):
    __slots__ = ("randomNumber", "serverMessage")
    RANDOMNUMBER_FIELD_NUMBER: _ClassVar[int]
    SERVERMESSAGE_FIELD_NUMBER: _ClassVar[int]
    randomNumber: int
    serverMessage: str
    def __init__(self, randomNumber: _Optional[int] = ..., serverMessage: _Optional[str] = ...) -> None: ...
