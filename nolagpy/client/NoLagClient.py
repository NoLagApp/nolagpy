import array
import websocket
import threading

from enum import Enum
from typing import Any, Callable, Optional, Tuple

from nolagpy.shared.constants import CONSTANT

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
        self.callbackOnReceive = lambda _: None
        self.callbackOnClose = lambda _: None
        self.callbackOnError = lambda _: None

    def isBrowser(self):
        return False

    async def connect(self) -> Any:
        self.connectionStatus = IDLE
        return await self.nodeInstance()

    def disconnect(self):
        if self.wsInstance and self.wsInstance.connected:
            self.wsInstance.close()

    async def nodeInstance(self):
        self.environment = EEnvironment.Nodejs
        if self.connectionStatus == CONNECTED:
            return

        def on_open(ws):
            print("Opened connection")

        def on_message(ws, message):
            print(f"on_message: {message}")
            self._onReceive(message)

        def on_close(ws, one, two):
            print(f"on_close: {ws}")
            print(f"one: {one}")
            print(f"two: {two}")
            print("### closed ###")
            self._onClose(None)

        def on_error(ws, error):
            self._onError(error)

        self.wsInstance = websocket.WebSocketApp(
            f"{self.protocol}://{self.host}{self.url}",
            on_open=on_open,
            on_message=on_message,
            on_close=on_close,
            on_error=on_error
        )
        # self.wsInstance.connect("ws://echo.websocket.events/")
        websocket.enableTrace(True)
        wst = threading.Thread(target=self.wsInstance.run_forever)
        wst.daemon = True
        wst.start()
        while True:
            if (self.connectionStatus != IDLE):
                print(55555555)
                break
        # asyncio.get_event_loop().run_until_complete(self.wsInstance)
        # asyncio.get_event_loop().run_forever()
        # self.wsInstance.run_forever()

    @property
    def status(self):
        return self.connectionStatus.value

    def authenticate(self):
        self.connectionStatus = CONNECTING
        encoded = self.authToken.encode()
        array = bytearray(encoded)
        self.send(bytes(self.authToken, "utf-8"))

    def onOpen(self, callback: FConnection):
        self.callbackOnOpen = callback

    def onReceiveMessage(self, callback: FConnection):
        self.callbackOnReceive = callback

    def onClose(self, callback: FConnection):
        self.callbackOnClose = callback

    def onError(self, callback: FConnection):
        self.callbackOnError = callback

    def _onOpen(self, _):
        self.connectionStatus = IDLE
        self.callbackOnOpen(None)

    def getAlertMessage(self, payload: bytes) -> IErrorMessage:
        codeSplit = payload.find(EEnvironment.Browser.value)
        code = int(payload[:codeSplit])
        msg = payload[codeSplit + 1:].decode()
        return IErrorMessage(code, msg)

    def getGroupSeparatorIndex(self, payload: bytes) -> int:
        return payload.find(GROUP_SEPARATOR)

    def getGroups(self, payload: bytes) -> Tuple[bytes, bytes]:
        sliceIndex = self.getGroupSeparatorIndex(payload)
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
        topicAndIdentifiers, data = self.getGroups(payload)
        topicName, nqlIdentifiers = self.getRecords(topicAndIdentifiers)
        return IResponse(data, topicName, nqlIdentifiers)

    def _onReceive(self, data: bytes):
        if not data:
            return
        if data == CONNECTING and self.connectionStatus == IDLE:
            self.authenticate()
            return

        if data == CONNECTED and self.connectionStatus == CONNECTING:
            self.connectionStatus = CONNECTED
            self.deviceTokenId = data[2:]
            return
        if data == NEGATIVE_ACK_SEPARATOR:
            self.connectionStatus = CONNECTED
            self.callbackOnError(self.getAlertMessage(data))
            return
        self.callbackOnReceive(self.decode(data))

    def _onClose(self, error):
        self.connectionStatus = DISCONNECTED
        self.callbackOnClose(None)

    def _onError(self, error):
        self.connectionStatus = DISCONNECTED
        self.callbackOnError(error)

    def send(self, transport: bytes):
        if self.wsInstance:
            self.wsInstance.send_bytes(transport)

    def heartbeat(self):
        if self.wsInstance:
            self.wsInstance.send_bytes(b"")
