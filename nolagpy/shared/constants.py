from typing import Any, Callable, Optional, Tuple


CONSTANT = {
    "DefaultWsHost": "tunnel.nolag.app",
    "DefaultApiHost": "api.nolag.app",
    "DefaultWsUrl": "/ws",
    "DefaultPort": 443,
    "DefaultWsProtocol": "wss",
    "DefaultApiUrl": "/v1",
    "DefaultHttpProtocol": "https",
}

FConnection = Callable[[Optional[Any], Optional[Any]], None]

FAction = Callable[[Any], None]

TIdentifier = Tuple[str, str]

TIdentifiers = Tuple[str, str]

# In Python, there's no built-in ArrayBuffer type like in TypeScript.
# You can use bytes or bytearray to represent binary data.
# If you specifically need to deal with ArrayBuffer, you might need to handle it differently.
# For simplicity, I'll use bytes here.
TData = bytes

# In Python, dictionaries are already generic, so no need for a separate type.
# You can directly use a dictionary with any value type.
# If you want to specify types, you can use the `Dict` type from the `typing` module.
# dataType = Dict[str, T]
