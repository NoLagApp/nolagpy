from typing import Any, Dict, List, Protocol, Tuple

from requests import Session

# from nolagpy.api import ApiTunnel
from nolagpy.api.controllers.tunnels.TunnelDevice import ITunnelDevice, TunnelDevice
from nolagpy.api.controllers.tunnels.TunnelPublish import tunnelPublish
from nolagpy.api.controllers.tunnels.TunnelTopic import ITunnelTopic, TunnelTopic
from nolagpy.shared.interfaces import IHttpPublish


class ITunnelApi(Protocol):
    topics: ITunnelTopic
    devices: ITunnelDevice

    def publish(self, httpPublish: IHttpPublish) -> bool:
        pass


class TunnelApi:
    def __init__(self, apiTunnel: Any, tunnelId: str, request: Session):
        self.routeNamespace = "tunnels"
        self.tunnelId = tunnelId
        self.request = request
        self.apiTunnel = apiTunnel

    @property
    def topics(self) -> TunnelTopic:
        return TunnelTopic(self.routeNamespace, self.tunnelId, self.request)

    @property
    def devices(self) -> TunnelDevice:
        return TunnelDevice(self.routeNamespace, self.tunnelId, self.request)

    async def publish(self, httpPublish: IHttpPublish) -> bool:
        data, tunnelName, identifiers = httpPublish.data, httpPublish.tunnelName, httpPublish.identifiers
        return tunnelPublish(data, tunnelName, identifiers, self.tunnelId, self.routeNamespace, self.request, self.apiTunnel.connectOptions)
