import os
import json
from hashlib import sha256
import hmac
from ellipticcurve.utils.binary import numberFromByteString
import base64
def string_to_base64(input_string):
    """Encode a string to Base64."""
    byte_data = input_string.encode('utf-8')
    base64_bytes = base64.b64encode(byte_data)
    base64_string = base64_bytes.decode('utf-8')
    return base64_string

def base64_to_string(base64_string):
    """Decode a Base64 string."""
    base64_bytes = base64_string.encode('utf-8')
    byte_data = base64.b64decode(base64_bytes)
    decoded_string = byte_data.decode('utf-8')
    return decoded_string
class OTP:
    @classmethod
    def generate_key_from_password(cls,password, hashlib=sha256):
        """Generate a key from a password using Sha256."""

        key = hashlib(bytes(password)).digest()

        return str(numberFromByteString(key))
    @classmethod
    def encrypt(cls,plaintext, key):
        """Encrypt the plaintext using the key."""
        ciphertext = bytearray()
        for i in range(len(plaintext)):
            ciphertext.append(plaintext[i] ^ key[i % len(key)])
        return string_to_base64(bytes(ciphertext).decode("utf-8"))
    @classmethod
    def decrypt(cls,ciphertextbase64, key):
        """Decrypt the ciphertext using the key."""
        ciphertext= base64_to_string(ciphertextbase64).encode('utf-8')
        
        plaintext = bytearray()
        for i in range(len(ciphertext)):
            plaintext.append(ciphertext[i] ^ key[i % len(key)])
        return bytes(plaintext).decode("utf-8")