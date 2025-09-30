from .binaryformatter import deserialize, serialize
from .crypto import decrypt, encrypt


def read_save_data(data: bytes, use_encryption: bool = True) -> str:
    """Read and optionally decrypt save data from a byte stream.

    :param data: The byte stream containing the save data
    :param use_encryption: Whether to use decryption (default is True)
    """
    if use_encryption:
        deserialized_data = deserialize(data)
        return decrypt(deserialized_data)
    else:
        return data.decode("utf-8")


def write_save_data(data: str, use_encryption: bool = True) -> bytes:
    """Serialize and optionally encrypt save data to a byte stream.

    :param data: The save data as a string
    :param use_encryption: Whether to encrypt the data (default is True)
    """
    if use_encryption:
        encrypted_data = encrypt(data)
        return serialize(encrypted_data)
    else:
        return data.encode("utf-8")
