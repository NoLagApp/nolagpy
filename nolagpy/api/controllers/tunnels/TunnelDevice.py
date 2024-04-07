from typing import Any
from requests import Session
from nolagpy.shared.interfaces import IDeviceListQuery, IDeviceTokenModel, IPaginated
from nolagpy.shared.utils.generateQueryString import generateQueryString


class ITunnelDevice:
    def createDevice(self, payload: IDeviceTokenModel) -> IDeviceTokenModel:
        pass

    def getDeviceById(self, device_token_id: str) -> IDeviceTokenModel:
        pass

    def listDevices(self, query: IDeviceListQuery) -> Any:
        pass

    def updateDevice(self, device_token_id: str, payload: IDeviceTokenModel) -> IDeviceTokenModel:
        pass

    def deleteDevice(self, device_token_id: str) -> IDeviceTokenModel:
        pass


class TunnelDevice(ITunnelDevice):
    def __init__(self, parent_route_namespace: str, tunnel_id: str, request: Session):
        self.route_namespace = "devices"
        self.parent_route_namespace = parent_route_namespace
        self.tunnel_id = tunnel_id
        self.request = request

    def createDevice(self, payload: IDeviceTokenModel) -> IDeviceTokenModel:
        response = self.request.post(
            f"/{self.parent_route_namespace}/{self.tunnel_id}/{self.route_namespace}",
            json=payload  # Use json parameter for POST request
        )
        response.raise_for_status()  # Raise error if request fails
        return response.json()

    def getDeviceById(self, device_token_id: str) -> IDeviceTokenModel:
        response = self.request.get(
            f"/{self.parent_route_namespace}/{self.tunnel_id}/{self.route_namespace}/{device_token_id}"
        )
        response.raise_for_status()
        return response.json()

    def listDevices(self, query: IDeviceListQuery) -> Any:
        query_string = generateQueryString(query)
        response = self.request.get(
            f"/{self.parent_route_namespace}/{self.tunnel_id}/{self.route_namespace}{query_string}"
        )
        response.raise_for_status()
        return response.json()

    def updateDevice(self, device_token_id: str, payload: IDeviceTokenModel) -> IDeviceTokenModel:
        response = self.request.patch(
            f"/{self.parent_route_namespace}/{self.tunnel_id}/{self.route_namespace}/{device_token_id}",
            json=payload  # Use json parameter for PATCH request
        )
        response.raise_for_status()
        return response.json()

    def deleteDevice(self, device_token_id: str) -> IDeviceTokenModel:
        response = self.request.delete(
            f"/{self.parent_route_namespace}/{self.tunnel_id}/{self.route_namespace}/{device_token_id}"
        )
        response.raise_for_status()
        return response.json()
