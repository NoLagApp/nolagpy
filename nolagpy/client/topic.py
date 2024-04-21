from typing import Any, Callable, Dict, List, Optional
from nolagpy.client import NoLagClient
from nolagpy.shared.constants import TData
from nolagpy.shared.enums import EAction, ESeparator
from nolagpy.shared.interfaces import INqlIdentifiers, IResponse
from nolagpy.shared.utils.transport import (
    arrayOfString,
    generateTransport,
    nqlPayload,
    topicPayload,
    toRecordSeparator,
)


class ITopic:
    def addIdentifiers(self, identifiers: INqlIdentifiers) -> 'Topic': ...
    def removeIdentifiers(self, identifiers: List[str]) -> 'Topic': ...
    def unsubscribe(self) -> bool: ...

    def onReceive(self, callbackFn: Optional[Callable[[IResponse], None]]) -> 'Topic':
        ...

    def publish(self, data: TData, identifiers: List[str]) -> 'Topic': ...
    def reSubscribe(self) -> None: ...
    def _onReceiveMessage(self, data: IResponse) -> 'ITopic': ...


class Topic(ITopic):
    def __init__(self, connection: NoLagClient, topicName: str, identifiers: INqlIdentifiers):
        self.connection: Optional[NoLagClient] = None
        self.topicName: str = topicName
        self.callbackFn: Optional[Callable[[IResponse], None]] = None
        self.identifiers: List[str] = []
        self.setConnection(connection)
        self.saveIdentifiers(identifiers.get('OR', []))
        self.subscribe(identifiers.get('OR', []))

    def findSavedIdentifier(self, identifier: str) -> Optional[str]:
        for saved_identifier in self.identifiers:
            if saved_identifier == identifier:
                return saved_identifier
        return None

    def saveIdentifiers(self, identifiers: List[str]) -> None:
        for identifier in identifiers:
            if not self.findSavedIdentifier(identifier):
                self.identifiers.append(identifier)

    def deleteSavedIdentifiers(self, identifiers: List[str]) -> None:
        self.identifiers = [
            identifier for identifier in self.identifiers if identifier not in identifiers]

    def subscribe(self, identifiers: List[str]) -> None:
        topic_name = topicPayload(self.topicName)
        nql = nqlPayload(arrayOfString(identifiers), EAction.Add)
        records = toRecordSeparator([topic_name, nql])
        if self.connection:
            self.connection.send(records)

    def reSubscribe(self) -> None:
        self.addIdentifiers({'OR': self.identifiers})

    def setConnection(self, connection: NoLagClient) -> 'Topic':
        self.connection = connection
        return self

    def _onReceiveMessage(self, data: IResponse) -> 'ITopic':
        if self.callbackFn:
            self.callbackFn(data)
        return self

    def onReceive(self, callbackFn: Optional[Callable[[IResponse], None]]) -> 'Topic':
        self.callbackFn = callbackFn
        return self

    def addIdentifiers(self, identifiers: INqlIdentifiers) -> 'Topic':
        self.saveIdentifiers(identifiers.get('OR', []))
        topic_name = topicPayload(self.topicName)
        nql = nqlPayload(arrayOfString(
            identifiers.get('OR', [])), EAction.Add)
        records = toRecordSeparator([topic_name, nql])
        if self.connection:
            self.connection.send(records)
        return self

    def removeIdentifiers(self, identifiers: List[str]) -> 'Topic':
        self.deleteSavedIdentifiers(identifiers)
        topic_name = topicPayload(self.topicName)
        nql = nqlPayload(arrayOfString(identifiers), EAction.Delete)
        records = toRecordSeparator([topic_name, nql])
        if self.connection:
            self.connection.send(records)
        return self

    def unsubscribe(self) -> bool:
        topic_name = topicPayload(self.topicName, EAction.Delete)
        nql = nqlPayload(b'')
        records = toRecordSeparator([topic_name, nql])
        if self.connection:
            self.connection.send(records)
        return True

    def publish(self, data: bytearray, identifiers: List[str]) -> 'Topic':
        transport = generateTransport(data, self.topicName, identifiers)
        if self.connection:
            self.connection.send(transport)
        return self
