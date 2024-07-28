from Cryptography.KeyFormats.RSA import RSAPrivateKey



privatekey = RSAPrivateKey(1024)

pubkey = privatekey.publickey

print(pubkey)
print(pubkey.json())

message="HELLO"
enc = pubkey.encrypt_string(message)
print(privatekey.decrypt_string(enc))