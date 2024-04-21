from enum import Enum


class EAction(Enum):
    Add = 'a'
    Delete = 'd'


class ESeparator(Enum):
    Group = 29
    Record = 30
    Unit = 31
    Vertical = 11
    NegativeAck = 21
    BellAlert = 7


def toUnitSeparator(unit_array):
    byte_length = 0

    #  add space for separator
    if len(unit_array) == 2:
        # total byte data
        # plus extra byte for separator
        byte_length = len(unit_array[0]) + len(unit_array[1]) + 1
    elif len(unit_array) == 1:
        byte_length = len(unit_array[0])

    unit_data = bytearray(byte_length)

    if len(unit_array) == 2:
        unit_data = toUint8Array(unit_data, unit_array[0], 0)
        unit_data[len(unit_array[0])] = ESeparator.Unit.value
        unit_data = toUint8Array(unit_data,
                                 unit_array[1], len(unit_array[0]) + 1)
    elif len(unit_array) == 1:
        unit_data = toUint8Array(unit_data, unit_array[0], 0)
    return bytes(unit_data)


def toUint8Array(uint8_array: bytearray, string: str, offset: int) -> bytearray:
    str_len = len(string)
    for i in range(str_len):
        uint8_array[offset] = ord(string[i])
        offset += 1
    return uint8_array


def topicPayload(topic_name, action: EAction = None):
    actionValue = action.value if action is not None else None
    return toUnitSeparator([item for item in [topic_name, actionValue] if item])


def nqlPayload(identifiers, action: EAction = None):
    actionValue = action.value if action is not None else None
    separator = 31
    action_string = actionValue.encode('utf-8') if action else bytes()
    return toTransportSeparator([identifiers, action_string], separator)


def toTransportSeparator(record_array, separator):
    byte_length = 0

    separator_array = bytes([separator])

    if record_array[0] and record_array[1] and record_array[1][0] is not None:
        byte_length = len(record_array[0]) + len(record_array[1]) + 1
    elif record_array[0]:
        byte_length = len(record_array[0])

    record_data = bytearray(byte_length)

    if record_array[0] and record_array[1] and record_array[1][0] is not None:
        record_data[:len(record_array[0])] = record_array[0]
        record_data[len(record_array[0]):len(
            record_array[0])+1] = separator_array
        record_data[len(record_array[0])+1:] = record_array[1]
    elif record_array[0]:
        record_data[:len(record_array[0])] = record_array[0]

    return bytes(record_data)


def arrayOfString(identifiers=None) -> bytes:
    #  count the number of characters found in all the identifiers
    #  we need this number to construct the Uint8Array
    identifiers = identifiers or []
    identifiers_length = sum(len(item) for item in identifiers)
    separator_length = len(identifiers) - 1 if len(identifiers) > 1 else 0
    uint8_length = identifiers_length + separator_length

    buf_view = bytearray(uint8_length)
    array_count = 0

    for item in identifiers:
        for char in item:
            buf_view[array_count] = ord(char)
            array_count += 1
        if identifiers[-1] != item:
            buf_view[array_count] = ESeparator.Vertical.value
            array_count += 1

    return bytes(buf_view)


def toRecordSeparator(record_array):
    return toTransportSeparator(record_array, ESeparator.Record.value)


def stringToUint8_array(string):
    buf_view = bytearray(len(string))
    for i, char in enumerate(string):
        buf_view[i] = ord(char)
    return bytes(buf_view)


def toGroupSeparator(records, data):
    separator_array = bytes([ESeparator.Group.value])
    bit_length = len(records) + len(separator_array) + len(data)
    buf = bytearray(bit_length)
    tmp = bytearray(buf)
    tmp[:len(records)] = records
    tmp[len(records):len(records)+1] = separator_array
    tmp[len(records)+1:] = data
    return bytes(tmp)


def generateTransport(data, topic_name, identifiers):
    topic_name_payload = topicPayload(topic_name)
    nql = nqlPayload(arrayOfString(identifiers))
    records = toRecordSeparator([topic_name_payload, nql])
    groups = toGroupSeparator(records, data)
    return groups
