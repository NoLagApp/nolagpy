def string_to_array_buffer(string: str) -> bytearray:
    buf = bytearray(len(string))
    for i in range(len(string)):
        buf[i] = ord(string[i])
    return buf


def uint8_array_to_string(data: bytearray) -> str:
    return "".join(chr(byte) for byte in data)
