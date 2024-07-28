from Cryptography.KeyFormats import Secp256k1PrivateKey


a = Secp256k1PrivateKey()

b = a.publickey

print(b)
print(b.json())