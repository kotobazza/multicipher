from ..Random import generate_random_number, generate_random_prime_number
from ..Math import extended_euclidean_algorithm, fast_power, EllipticCurve, EllipticCurvePoint, sha224hash

from pydantic import BaseModel



class Signature(BaseModel):
    r: int
    s: int
    hashed: int

    def __str__(self):
        return f"ECDSA_Signature(r={self.r}, s={self.s}, hash={self.hashed})"


class SignedMessage(BaseModel):
    message: str
    signature: Signature

    def __str__(self):
        return f"ECDSA_SignedMessage(message={self.message}, signature={self.signature.__str__()})"
    
    
    

class ECDSAPublicKey(BaseModel):
    subgroup_order: int
    public_key_point: EllipticCurvePoint
    generation_point: EllipticCurvePoint
    
    def check_signature(self, signed_message: SignedMessage) -> bool:
        sign = signed_message.signature
        
        assert(0 < sign.r and sign.r < self.subgroup_order)
        assert(0 < sign.s and sign.s < self.subgroup_order)

        e = sign.hashed % self.subgroup_order
        _, v, _ = extended_euclidean_algorithm(e, self.subgroup_order)

        z1 = sign.s*v%self.subgroup_order
        z2 = -sign.r*v%self.subgroup_order

        C = z1*self.generation_point + z2*self.public_key_point

        return C.x == sign.r

    def __str__(self):
        return f"ECDSA_PublicKey(generation_point={self.generation_point}, subgroup_order={self.subgroup_order}, pubkey_point={self.public_key_point})" 



class ECDSAPrivateKey:

    def __init__(self, subgroup_order, gp: EllipticCurvePoint):
        self.q = subgroup_order
        
        self.generation_point = gp 

        self.private_key = generate_random_number(3, self.q)
        self.public_key = self.private_key * self.generation_point

    def sign(self, signable:str, algorithm = sha224hash):
        hashed = algorithm(signable)
        signature = self.__sing_sha224hash(hashed)

        return SignedMessage(message=signable, signature=signature)

        
    
    def __sing_sha224hash(self, hashed:int):
        assert(hashed < self.q)
        e = hashed % self.q
        s = 0
        while s == 0:

            k = generate_random_number(0, self.q)
            C = k*self.generation_point

            r = C.x % self.q
            s = (r*self.private_key + k*e) % self.q

        return Signature(r = r, s = s, hashed = hashed)

    @property
    def publickey(self):
        return ECDSAPublicKey(subgroup_order=self.q, public_key_point=self.public_key, generation_point=self.generation_point)
        



class Secp256k1PrivateKey(ECDSAPrivateKey):
    
    def __init__(self):
        Secp256k1Curve = EllipticCurve(
            a = 0, 
            b=7, 
            p = 115792089237316195423570985008687907853269984665640564039457584007908834671663)
        Secp256k1GenerationPoint = EllipticCurvePoint(
            x = 55066263022277343669578718895168534326250603453777594175500187360389116729240,
            y = 32670510020758816978083085130507043184471273380659243275938904335757337482424,
            curve = Secp256k1Curve)


        Secp256k1SubgroupOrder = 115792089237316195423570985008687907852837564279074904382605163141518161494337
        super().__init__(Secp256k1SubgroupOrder, Secp256k1GenerationPoint)






