import struct

_SERIALIZATION_HEADER = struct.pack(
    "<Biiii",
    0x00,  # RecordType: SerializationHeaderRecord
    1,  # RootId
    -1,  # HeaderId
    1,  # MajorVersion
    0,  # MinorVersion
)

_STRING_RECORD_HEADER = struct.pack(
    "<Bi",
    0x06,  # RecordType: BinaryObjectString
    1,  # ObjectId
)

_DATA_HEADER = _SERIALIZATION_HEADER + _STRING_RECORD_HEADER

_MESSAGE_END = struct.pack("<B", 0x0B)


def _encode_7bit_int(value: int) -> bytes:
    """Encode an integer as 7-bit format byte string.

    :param value: The integer to encode
    :return: The encoded bytes
    """
    if value < 0:
        raise ValueError("Length cannot be negative.")
    if value == 0:
        return b"\x00"

    buffer = bytearray()
    while value > 0:
        byte = value & 0x7F
        value >>= 7
        if value > 0:
            byte |= 0x80  # Set the highest bit to indicate more bytes follow
        buffer.append(byte)
    return bytes(buffer)


def _decode_7bit_int(stream: bytes, offset: int) -> tuple[int, int]:
    """Decode a 7-bit integer from the specified offset in a byte stream.

    :param stream: The byte stream to decode from
    :param offset: The offset position to start decoding
    :return: A tuple containing the decoded integer and the new offset position
    :raises ValueError: If the encoded integer is invalid or too large
    """
    result = 0
    shift = 0
    current_offset = offset

    while True:
        if current_offset >= len(stream):
            raise ValueError("Invalid 7-bit encoded integer: unexpected end of stream.")

        byte = stream[current_offset]
        result |= (byte & 0x7F) << shift
        current_offset += 1

        if (byte & 0x80) == 0:
            break  # Highest bit is 0, indicating this is the last byte

        shift += 7
        if shift >= 64:  # Prevent infinite loops and overflow
            raise ValueError("Invalid 7-bit encoded integer: number is too large.")

    return result, current_offset


def serialize(text: str) -> bytes:
    """Serialize a Python string to BinaryFormatter binary format.

    :param text: The string to serialize
    :return: A bytes object representing the serialized string
    """
    encoded_text = text.encode("utf-8")
    encoded_length = _encode_7bit_int(len(encoded_text))

    return _DATA_HEADER + encoded_length + encoded_text + _MESSAGE_END


def deserialize(data: bytes) -> str:
    """Deserialize binary data from BinaryFormatter to a Python string.

    :param data: The binary data to deserialize
    :return: The deserialized string
    :raises ValueError: If the input data format is incorrect
    """
    if not data.startswith(_DATA_HEADER):
        raise ValueError("Invalid BinaryFormatter data format.")

    offset = len(_DATA_HEADER)
    length, offset = _decode_7bit_int(data, offset)

    if offset + length > len(data):
        raise ValueError("Invalid string data.")

    return data[offset : offset + length].decode("utf-8")
