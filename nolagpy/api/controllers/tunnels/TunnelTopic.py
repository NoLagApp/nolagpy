from typing import Dict, Any
from requests import Session
from src.shared.interfaces import ITopicQuery, ITopicModel, IPaginated
from src.shared.utils.generateQueryString import generateQueryString


class ITunnelTopic:
    def createTopic(self, payload: ITopicModel) -> ITopicModel:
        pass

    def getTopicById(self, topicId: str) -> ITopicModel:
        pass

    def listTopics(self, query: ITopicQuery) -> Any:
        pass

    def updateTopic(self, topicId: str, payload: ITopicModel) -> ITopicModel:
        pass

    def deleteTopic(self, topicId: str) -> ITopicModel:
        pass


class TunnelTopic(ITunnelTopic):
    def __init__(self, parent_route_namespace: str, tunnel_id: str, request: Session):
        self.route_namespace = "Topics"
        self.parent_route_namespace = parent_route_namespace
        self.tunnel_id = tunnel_id
        self.request = request

    def createTopic(self, payload: ITopicModel) -> ITopicModel:
        response = self.request.post(
            f"/{self.parent_route_namespace}/{self.tunnel_id}/{self.route_namespace}",
            json=payload
        )
        return response.json()

    def getTopicById(self, topicId: str) -> ITopicModel:
        response = self.request.get(
            f"/{self.parent_route_namespace}/{self.tunnel_id}/{self.route_namespace}/{topicId}"
        )
        return response.json()

    def listTopics(self, query: ITopicQuery) -> Any:
        query_string = generateQueryString(query)
        response = self.request.get(
            f"/{self.parent_route_namespace}/{self.tunnel_id}/{self.route_namespace}{query_string}"
        )
        return response.json()

    def updateTopic(self, topicId: str, payload: ITopicModel) -> ITopicModel:
        response = self.request.patch(
            f"/{self.parent_route_namespace}/{self.tunnel_id}/{self.route_namespace}/{topicId}",
            json=payload
        )
        return response.json()

    def deleteTopic(self, topicId: str) -> ITopicModel:
        response = self.request.delete(
            f"/{self.parent_route_namespace}/{self.tunnel_id}/{self.route_namespace}/{topicId}"
        )
        return response.json()
