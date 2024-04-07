from typing import List, Union, Dict, Any
from requests import Session
from src.shared.constants import TData
from src.shared.interfaces import IConnectOptions
from src.shared.utils.transport import generateTransport

route_namespace = "publish"


def tunnelPublish(data: TData, topic_name: str, identifiers: List[str],
                  tunnel_id: str, parent_route_namespace: str,
                  request: Session, connect_options: IConnectOptions) -> bool:
    transport = generateTransport(data, topic_name, identifiers)
    request.post(
        f"/{parent_route_namespace}/{tunnel_id}/{route_namespace}",
        headers={"Content-Type": "application/json"},
        data=transport,
        baseURL=f"{connect_options.protocol}://{connect_options.wsHost}"
    )
    return True
