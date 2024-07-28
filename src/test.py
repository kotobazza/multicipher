from Cryptography.Math import EllipticCurve, EllipticCurvePoint
from Cryptography.KeyFormats.ECDSA import ECDSAPrivateKey



subgroup_order=57896044618658097711785492504343953927082934583725450622380973592137631069619
a = 7
b = 43308876546767276905765904595650931995942111794451039583252968842033849580414
p = 57896044618658097711785492504343953926634992332820282019728792003956564821041
x = 2
y = 4018974056539037503335449422937059775635739389905545080690979365213431566280



curve = EllipticCurve(a=a, b=b, p=p)

generation_point = EllipticCurvePoint(x=x, y=y, curve=curve)

privatekey = ECDSAPrivateKey(subgroup_order, generation_point)

publickey = privatekey.publickey

print(publickey)
print()
print(publickey.json())
print()

print()

sign = privatekey.sign("HelloWorld")
print(sign)
print()
print(sign.json())
print()

print(publickey.check_signature(sign))
print()