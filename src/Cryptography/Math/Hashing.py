import hashlib
import base64
import zlib

def sha224hash(string:str):
    m = hashlib.sha224()
    m.update(string.encode("utf-8"))
    hashed = int(m.hexdigest(), 16)
    return hashed

def base64zlibencode(message:str):
    message_bytes = message.encode('utf-8')
    compressed_bytes = zlib.compress(message_bytes)
    base64_bytes = base64.b64encode(compressed_bytes)
    message_int = int.from_bytes(base64_bytes, byteorder='big')
    return message_int
    
def base64zlibdecode(message:int):
    base64_bytes = message.to_bytes((message.bit_length() + 7) // 8, byteorder='big')
    compressed_bytes = base64.b64decode(base64_bytes)
    message_bytes = zlib.decompress(compressed_bytes)
    message = message_bytes.decode('utf-8')
    return message