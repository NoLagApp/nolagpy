import websocket
import threading

from enum import Enum
from typing import Any, Callable, Optional, Tuple

from src.shared.constants import CONSTANT

# Define Enums


class EConnectionStatus(Enum):
    Idle = "Idle"
    Connecting = "Connecting"
    Connected = "Connected"
    Disconnected = "Disconnected"


class EEncoding(Enum):
    Arraybuffer = "arraybuffer"


class EEnvironment(Enum):
    Browser = "Browser"
    Nodejs = "Nodejs"


BELL_ALERT = b'\x07'
GROUP_SEPARATOR = b'\x1D'
RECORD_SEPARATOR = b'\x1E'
NEGATIVE_ACK_SEPARATOR = b'\x15'

IDLE = "idle"
CONNECTING = b'\x06'
CONNECTED = b'\x06\x06'
DISCONNECTED = b'\x06\x06\x06'

# Define Interfaces


class IConnectOptions:
    def __init__(self, host: Optional[str] = None, protocol: Optional[str] = None,
                 checkConnectionInterval: Optional[int] = None, checkConnectionTimeout: Optional[int] = None):
        self.host = host
        self.protocol = protocol
        self.checkConnectionInterval = checkConnectionInterval
        self.checkConnectionTimeout = checkConnectionTimeout


class IErrorMessage:
    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg


class IResponse:
    def __init__(self, data: bytes, topicName: str, nqlIdentifiers: Tuple[str]):
        self.data = data
        self.topicName = topicName
        self.nqlIdentifiers = nqlIdentifiers


# Define callback type
FConnection = Callable[[Optional[IErrorMessage], Optional[IResponse]], None]


class NoLagClient:
    def __init__(self, authToken: str, connectOptions: Optional[IConnectOptions] = None):
        self.authToken = authToken
        self.host = connectOptions.host if connectOptions and connectOptions.host else CONSTANT.get(
            "DefaultWsHost")
        self.protocol = connectOptions.protocol if connectOptions and connectOptions.protocol else CONSTANT.get(
            "DefaultWsProtocol")
        self.url = CONSTANT.get(
            "DefaultWsUrl")
        self.checkConnectionInterval = connectOptions.checkConnectionInterval if connectOptions and connectOptions.checkConnectionInterval else 100
        self.checkConnectionTimeout = connectOptions.checkConnectionTimeout if connectOptions and connectOptions.checkConnectionTimeout else 10000

        self.wsInstance = None
        self.deviceConnectionId = None
        self.environment = None
        self.deviceTokenId = None
        self.connectionStatus = IDLE

        self.callbackOnOpen = lambda _: None
        self.callbackOnReceive = lambda _, __: None
        self.callbackOnClose = lambda _: None
        self.callbackOnError = lambda _: None

    def isBrowser(self):
        return False

    async def connect(self) -> Any:
        self.connectionStatus = IDLE
        return self.nodeInstance()

    def disconnect(self):
        if self.wsInstance and self.wsInstance.connected:
            self.wsInstance.close()

    def nodeInstance(self):
        self.environment = EEnvironment.Nodejs
        if self.connectionStatus == CONNECTED:
            return

        def on_open(ws):
            self._onOpen(None)

        def on_message(ws, message):
            print(message)
            self._onReceive(message)

        def on_close(ws):
            self._onClose(None)

        def on_error(ws, error):
            self._onError(error)

        print(f"{self.protocol}://{self.host}{self.url}")
        self.wsInstance = websocket.WebSocketApp(
            f"{self.protocol}://{self.host}{self.url}",
            on_open=on_open,
            on_message=on_message,
            on_close=on_close,
            on_error=on_error
        )
        self.wsInstance.run_forever()

    @property
    def status(self):
        return self.connectionStatus.value

    def authenticate(self):
        self.connectionStatus = CONNECTING
        self.send(self.authToken.encode())

    def onOpen(self, callback: FConnection):
        self.callbackOnOpen = callback

    def onReceiveMessage(self, callback: FConnection):
        self.callbackOnReceive = callback

    def onClose(self, callback: FConnection):
        self.callbackOnClose = callback

    def onError(self, callback: FConnection):
        self.callbackOnError = callback

    def _onOpen(self, _):
        self.connectionStatus = CONNECTED
        self.callbackOnOpen(None)

    def getAlertMessage(self, payload: bytes) -> IErrorMessage:
        codeSplit = payload.find(EEnvironment.Browser.value)
        print(payload[:codeSplit])
        code = int(payload[:codeSplit])
        msg = payload[codeSplit + 1:].decode()
        return IErrorMessage(code, msg)

    def getGroupSeparatorIndex(self, payload: bytes) -> int:
        print(f"getGroupSeparatorIndex1: {type(payload)}")
        print(
            f"getGroupSeparatorIndex2: {payload.find(GROUP_SEPARATOR)}")
        return payload.find(GROUP_SEPARATOR)

    def getGroups(self, payload: bytes) -> Tuple[bytes, bytes]:
        sliceIndex = self.getGroupSeparatorIndex(payload)

        print(f"sliceIndex: {sliceIndex}")
        topicAndIdentifiers = payload[:sliceIndex]
        data = payload[sliceIndex + 1:]
        return topicAndIdentifiers, data

    def getRecordSeparatorIndex(self, payload: bytes) -> int:
        return payload.find(RECORD_SEPARATOR)

    def getRecords(self, payload: bytes) -> Tuple[str, Tuple[str]]:
        sliceIndex = self.getRecordSeparatorIndex(payload)

        topicName = payload[:sliceIndex].decode()
        nqlIdentifiers = tuple(payload[sliceIndex + 1:].decode().split("|"))
        return topicName, nqlIdentifiers

    def decode(self, payload: bytes) -> IResponse:
        print(f"payload 1: {payload}")
        topicAndIdentifiers, data = self.getGroups(payload)
        topicName, nqlIdentifiers = self.getRecords(topicAndIdentifiers)
        print(f"payload: {payload}")
        return IResponse(data, topicName, nqlIdentifiers)

    def _onReceive(self, message: bytes):
        print(message)
        data = message
        if not data:
            return
        print(f"payload: {type(data)}")
        print(f"payload: {data}")
        print(f"payload: {type(CONNECTING)}")
        print(f"payload: {CONNECTING}")
        print(f"{data == CONNECTING}")
        if data[0] == CONNECTING and self.connectionStatus == IDLE:
            self.authenticate()
            return

        print(data[:2])
        if data[:2] == CONNECTED and self.connectionStatus == CONNECTING:
            self.connectionStatus = CONNECTED
            self.deviceTokenId = data[2:]
            return
        print(data[:2])
        if data[0] == NEGATIVE_ACK_SEPARATOR:
            self.connectionStatus = CONNECTED
            self.callbackOnError(self.getAlertMessage(data))
            return
        print(f"decode: {self.decode(data)}")
        self.callbackOnReceive(self.decode(data))

    def _onClose(self, error):
        print(f"close:{error}")
        self.connectionStatus = DISCONNECTED
        self.callbackOnClose(None)

    def _onError(self, error):
        print(f"error:{error}")
        self.connectionStatus = DISCONNECTED
        self.callbackOnError(error)

    def send(self, transport: bytes):
        if self.wsInstance:
            self.wsInstance.send(transport)

    def heartbeat(self):
        if self.wsInstance:
            self.wsInstance.send(b"")
