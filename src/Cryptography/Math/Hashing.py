import hashlib

def sha224hash(string:str):
    m = hashlib.sha224()
    m.update(string.encode("utf-8"))
    hashed = int(m.hexdigest(), 16)
    return hashed