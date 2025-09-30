import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

_KEY = b"UKu52ePUBwetZ9wNX88o54dnfKRu0T1l"  # 32 bytes for AES-256


def encrypt(data: str) -> str:
    """Encrypt the given string data using AES encryption.

    :param data: The string data to encrypt
    :return: The encrypted data as a base64-encoded string
    """
    cipher = AES.new(_KEY, AES.MODE_ECB)
    padded_data = pad(data.encode("utf-8"), AES.block_size)
    encrypted_bytes = cipher.encrypt(padded_data)
    return base64.b64encode(encrypted_bytes).decode("utf-8")


def decrypt(encrypted_data: str) -> str:
    """Decrypt the given encrypted data using AES decryption.

    :param encrypted_data: The encrypted data as a base64-encoded string
    :return: The decrypted string data
    """
    cipher = AES.new(_KEY, AES.MODE_ECB)
    decoded_data = base64.b64decode(encrypted_data)
    decrypted_bytes = unpad(cipher.decrypt(decoded_data), AES.block_size)
    return decrypted_bytes.decode("utf-8")
