import requests
from typing import Optional
from nolagpy.api.controllers.tunnels.TunnelApi import ITunnelApi, TunnelApi
from nolagpy.shared.constants import CONSTANT
from nolagpy.shared.interfaces import IConnectOptions


class IApiTunnel:
    def tunnels(self, tunnelId: str) -> ITunnelApi:
        pass


class ApiTunnel:
    def __init__(self, apiKey: str, connectOptions: Optional[IConnectOptions] = None):
        self.apiKey = apiKey
        self.connectOptions = {
            "host": CONSTANT["DefaultApiHost"],
            "protocol": CONSTANT["DefaultHttpProtocol"],
            "url": CONSTANT["DefaultApiUrl"],
            "wsUrl": CONSTANT["DefaultWsUrl"],
            "wsHost": CONSTANT["DefaultWsHost"],
            **(connectOptions or {})
        }
        self.request = self.createRequestInstance()

    def createRequestInstance(self):
        baseUrl = f"{self.connectOptions.get('protocol', 'https')}://{self.connectOptions.get('host', 'api.nolag.app')}{self.connectOptions.get('url', '/v1')}"
        headers = {
            "X-API-Key": self.apiKey,
            "Content-Type": "application/json"
        }
        session = requests.Session()
        adepter = requests.adapters.HTTPAdapter(max_retries=3)
        session.headers.update(headers)
        return session.mount(baseUrl, adepter)

    def tunnels(self, tunnelId: str) -> ITunnelApi:
        return TunnelApi(self, tunnelId, self.request)


def Api(apiKey: str, connectOptions: Optional[IConnectOptions] = None) -> IApiTunnel:
    return ApiTunnel(apiKey, connectOptions)
