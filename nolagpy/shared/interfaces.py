from typing import Any, Dict, List, Optional

# Constants from constants.ts
TData = Any

# Enumerations from enum.ts


class EAccessPermission:
    # Define the access permissions if necessary
    pass


class EStatus:
    # Define the status if necessary
    pass


class ETopicType:
    # Define the topic types if necessary
    pass


# Type alias from types.ts
dataType = Dict[str, Any]

# Interfaces


class ITunnelOptions:
    def __init__(self, disconnectOnNoVisibility: Optional[bool] = None):
        self.disconnectOnNoVisibility = disconnectOnNoVisibility


class IConnectOptions:
    def __init__(
        self,
        host: Optional[str] = None,
        wsHost: Optional[str] = None,
        port: Optional[int] = None,
        path: Optional[str] = None,
        protocol: Optional[str] = None,
        url: Optional[str] = None,
        wsUrl: Optional[str] = None,
        devMode: Optional[bool] = None,
        checkConnectionInterval: Optional[int] = None,
        checkConnectionTimeout: Optional[int] = None
    ):
        self.host = host
        self.wsHost = wsHost
        self.port = port
        self.path = path
        self.protocol = protocol
        self.url = url
        self.wsUrl = wsUrl
        self.devMode = devMode
        self.checkConnectionInterval = checkConnectionInterval
        self.checkConnectionTimeout = checkConnectionTimeout


class IResponse:
    def __init__(self, data: bytes, nqlIdentifiers: List[str], topicName: str):
        self.data = data
        self.nqlIdentifiers = nqlIdentifiers
        self.topicName = topicName


class IPagination:
    def __init__(
        self,
        page: Optional[int] = None,
        size: Optional[int] = None,
        hasPrevious: Optional[bool] = None,
        hasNext: Optional[bool] = None,
        total: Optional[int] = None
    ):
        self.page = page
        self.size = size
        self.hasPrevious = hasPrevious
        self.hasNext = hasNext
        self.total = total


class IPaginated:
    def __init__(self, records: List[Any], pagination: IPagination):
        self.records = records
        self.pagination = pagination


class IDeviceListQuery:
    def __init__(
        self,
        deviceAccessToken: Optional[str] = None,
        expireFromDate: Optional[int] = None,
        expireToDate: Optional[int] = None,
        name: Optional[str] = None,
        search: Optional[str] = None,
        size: Optional[int] = None,
        page: Optional[int] = None
    ):
        self.deviceAccessToken = deviceAccessToken
        self.expireFromDate = expireFromDate
        self.expireToDate = expireToDate
        self.name = name
        self.search = search
        self.size = size
        self.page = page


class IStaticTopic:
    def __init__(self, name: str, identifiers: Optional[List[str]] = None):
        self.name = name
        self.identifiers = identifiers


class IDeviceTokenModel:
    def __init__(
        self,
        name: str,
        accessPermission: EAccessPermission,
        deviceTokenId: Optional[str] = None,
        deviceAccessToken: Optional[str] = None,
        projectId: Optional[str] = None,
        tunnelId: Optional[str] = None,
        staticTopics: Optional[List[IStaticTopic]] = None,
        lockTopics: Optional[bool] = None,
        expireIn: Optional[int] = None,
        expireDate: Optional[int] = None
    ):
        self.name = name
        self.accessPermission = accessPermission
        self.deviceTokenId = deviceTokenId
        self.deviceAccessToken = deviceAccessToken
        self.projectId = projectId
        self.tunnelId = tunnelId
        self.staticTopics = staticTopics
        self.lockTopics = lockTopics
        self.expireIn = expireIn
        self.expireDate = expireDate


class IHttpPublish:
    def __init__(self, data: TData, tunnelName: str, identifiers: List[str]):
        self.data = data
        self.tunnelName = tunnelName
        self.identifiers = identifiers


class ITopicApiModel:
    def __init__(self, url: str, queryParams: Optional[dataType] = None, headers: Optional[dataType] = None):
        self.url = url
        self.queryParams = queryParams
        self.headers = headers


class ITopicModel:
    def __init__(
        self,
        topicId: Optional[str] = None,
        projectId: Optional[str] = None,
        tunnelId: Optional[str] = None,
        status: Optional[EStatus] = None,
        name: Optional[str] = None,
        triggerApi: Optional[ITopicApiModel] = None,
        hydrateApi: Optional[ITopicApiModel] = None,
        noEcho: Optional[bool] = None
    ):
        self.topicId = topicId
        self.projectId = projectId
        self.tunnelId = tunnelId
        self.status = status
        self.name = name
        self.triggerApi = triggerApi
        self.hydrateApi = hydrateApi
        self.noEcho = noEcho


class ITopicQuery:
    def __init__(
        self,
        topicId: Optional[str] = None,
        projectId: Optional[str] = None,
        tunnelId: Optional[str] = None,
        status: Optional[EStatus] = None,
        name: Optional[str] = None,
        size: Optional[int] = None,
        page: Optional[int] = None,
        search: Optional[str] = None
    ):
        self.topicId = topicId
        self.projectId = projectId
        self.tunnelId = tunnelId
        self.status = status
        self.name = name
        self.size = size
        self.page = page
        self.search = search


class IErrorsModel:
    def __init__(
        self,
        property: Optional[str] = None,
        value: Optional[str] = None,
        descriptions: Optional[List[str]] = None,
        errors: Optional[List['IErrorsModel']] = None
    ):
        self.property = property
        self.value = value
        self.descriptions = descriptions
        self.errors = errors


class IErrorMessage:
    def __init__(
        self,
        id: Optional[str] = None,
        code: Optional[int] = None,
        msg: Optional[str] = None,
        description: Optional[str] = None,
        errors: Optional[List[IErrorsModel]] = None
    ):
        self.id = id
        self.code = code
        self.msg = msg
        self.description = description
        self.errors = errors


class INqlIdentifiers:
    def __init__(self, OR: Optional[List[str]] = None):
        self.OR = OR
