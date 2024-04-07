from enum import Enum


# class EConnectionStatus(Enum):
#     Idle = "idle"
#     Connecting = b'x06'
#     Connected = b'x06x06'
#     Disconnected = b'x06x06x06'


class EEnvironment(Enum):
    Nodejs = "nodejs"
    Browser = "browser"


class EAction(Enum):
    Add = "a"
    Delete = "d"


class EEncoding(Enum):
    Arraybuffer = "arraybuffer"


class EVisibilityState(Enum):
    Hidden = "hidden"
    Visible = "visible"


class ESeparator(Enum):
    Group = 29
    Record = 30
    Unit = 31
    Vertical = 11
    NegativeAck = 21
    BellAlert = 7


class EAccessPermission(Enum):
    Subscribe = "subscribe"
    Publish = "publish"
    PubSub = "pubSub"


class EStatus(Enum):
    Active = "active"
    Inactive = "inactive"


class ETopicType(Enum):
    Standard = "standard"
    Api = "api"
