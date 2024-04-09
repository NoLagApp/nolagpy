from enum import Enum
import threading
from typing import Any, Callable, Dict, List, Optional, Tuple
from nolagpy.shared.interfaces import IConnectOptions, IErrorMessage, INqlIdentifiers, IResponse, ITunnelOptions
from nolagpy.shared.constants import FConnection, TData
from nolagpy.shared.types import dataType
from .topic import ITopic, Topic
from .NoLagClient import NoLagClient
from nolagpy.shared.enums import EVisibilityState
from nolagpy.shared.utils.transport import generateTransport


class EConnectionStatus(Enum):
    Idle = "Idle"
    Connecting = "Connecting"
    Connected = "Connected"
    Disconnected = "Disconnected"


class Tunnel:
    def __init__(self, authToken: str, options: Optional[ITunnelOptions] = None, connectOptions: Optional[IConnectOptions] = None):
        self.noLagClient: Optional[NoLagClient] = None
        self.connectOptions: Optional[IConnectOptions] = connectOptions
        self.authToken: str = authToken
        self.topics: Dict[str, ITopic] = {}
        self.heartbeatTimer: threading.Timer = None
        self.defaultCheckConnectionInterval: int = 10000
        self.checkConnectionInterval: int = connectOptions.checkConnectionInterval if connectOptions and connectOptions.checkConnectionInterval else self.defaultCheckConnectionInterval
        self.reconnectAttempts: int = 0
        self.maxReconnectAttempts: int = 5
        self.heartBeatInterval: int = 20000
        self.visibilityState: str = EVisibilityState.Visible
        self.callbackOnReceive: Optional[Callable[[IResponse], None]] = None
        self.callbackOnDisconnect: FConnection = lambda _: None
        self.callbackOnReconnect: FConnection = lambda _: None
        self.callbackOnReceivedError: FConnection = lambda _: None

    @property
    def deviceTokenId(self) -> Optional[str]:
        return self.noLagClient.deviceTokenId if self.noLagClient else None

    def startHeartbeat(self) -> None:
        self.heartbeatTimer = threading.Timer(
            self.heartBeatInterval, self.startHeartbeat
        )
        self.heartbeatTimer.start()
        if self.noLagClient:
            self.noLagClient.heartbeat()

    def stopHeartbeat(self) -> None:
        if self.heartbeatTimer:
            self.heartbeatTimer.cancel()

    def reSubscribe(self) -> None:
        for topic in self.topics.values():
            topic.reSubscribe()

    async def initiate(self) -> None:
        self.noLagClient = NoLagClient(self.authToken, self.connectOptions)
        await self.noLagClient.connect()
        self.resetConnectAttempts()
        self.startHeartbeat()
        self.reSubscribe()

    def resetConnectAttempts(self) -> None:
        self.reconnectAttempts = 0

    def handleReceiveMessage(self, data: IResponse) -> None:
        topicName = data.topicName
        if topicName and topicName in self.topics:
            self.topics[topicName]._onReceiveMessage(data)
        if self.callbackOnReceive:
            self.callbackOnReceive(data)

    def handleOnClose(self, err: Any, data: IResponse) -> None:
        self.doReconnect()
        if self.callbackOnReceivedError:
            self.callbackOnReceivedError(err)

    def handleOnError(self, err: IErrorMessage, data: IResponse) -> None:
        if self.callbackOnReceivedError:
            self.callbackOnReceivedError(err)

    def reconnect(self) -> None:
        self.stopHeartbeat()
        threading.Timer(self.checkConnectionInterval, self.initiate).start()
        self.reconnectAttempts += 1
        if self.callbackOnReconnect:
            self.callbackOnReconnect()

    def canReconnect(self) -> bool:
        return self.reconnectAttempts < self.maxReconnectAttempts and self.visibilityState == EVisibilityState.Visible

    def doReconnect(self) -> None:
        if self.canReconnect():
            self.reconnect()
        else:
            self.stopHeartbeat()
            if self.callbackOnDisconnect:
                self.callbackOnDisconnect("connection retry timeout.")

    def onClose(self) -> None:
        self.noLagClient.onClose(self.handleOnClose)

    def onError(self) -> None:
        self.noLagClient.onError(self.handleOnError)

    def onReceive(self, callback: Callable[[IResponse], None]) -> None:
        self.callbackOnReceive = callback

    def disconnect(self) -> None:
        self.reconnectAttempts = 5
        self.noLagClient.disconnect()

    def onDisconnect(self, callback: FConnection) -> None:
        self.callbackOnDisconnect = callback

    def onReconnect(self, callback: FConnection) -> None:
        self.callbackOnReconnect = callback

    def onErrors(self, callback: FConnection) -> None:
        self.callbackOnReceivedError = callback

    def getTopic(self, topicName: str) -> Optional[ITopic]:
        if topicName not in self.topics and self.noLagClient:
            self.topics[topicName] = Topic(self.noLagClient, topicName, {})
        return self.topics.get(topicName, None)

    def unsubscribe(self, topicName: str) -> bool:
        if topicName in self.topics:
            self.topics[topicName].unsubscribe()
            del self.topics[topicName]
            return True
        return False

    def subscribe(self, topicName: str, identifiers: INqlIdentifiers = {}) -> Optional[ITopic]:
        if self.noLagClient:
            print("has client")
            if topicName in self.topics:
                self.topics[topicName].reSubscribe()
                return self.topics[topicName]
            else:
                self.topics[topicName] = Topic(
                    self.noLagClient, topicName, identifiers)
                print(f"topicName: {topicName}")
                return self.topics[topicName]

    def publish(self, topicName: str, data: bytearray, identifiers: List[str] = []) -> None:
        if self.noLagClient and self.noLagClient.send:
            self.stopHeartbeat()
            transport = generateTransport(data, topicName, identifiers)
            self.noLagClient.send(transport)
            self.startHeartbeat()

    @property
    def status(self) -> Optional[str]:
        return self.noLagClient.status if self.noLagClient else None


async def WebSocketClient(authToken: str, options: Optional[ITunnelOptions] = None, connectOptions: Optional[IConnectOptions] = None) -> Tunnel:
    instance = Tunnel(authToken, options, connectOptions)
    await instance.initiate()
    return instance
