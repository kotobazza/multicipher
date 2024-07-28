from ..Random import generate_random_number, generate_random_prime_number
from ..Math import fast_power, extended_euclidean_algorithm, base64zlibdecode, base64zlibencode
from pydantic import BaseModel




class RSAPrivateKey:
    bits: int
    modulus: int
    public_part: int
    __private_part: int

    _p: int
    _q: int
    _phi: int
    
    def __init__(self, bits):
        self.bits = bits
        min_number_size = 2<<int(bits/2-1)
        max_number_size = 2<<int(bits/2)

        self._p = generate_random_prime_number(min_number_size, max_number_size)
        self._q = generate_random_prime_number(min_number_size, max_number_size)

        self.modulus = self._p*self._q
        
        self._phi = (self._p - 1) * (self._q - 1)
        self.public_part = generate_random_number(2, self._phi)

        while True:
            gcd, d, _ = extended_euclidean_algorithm(self.public_part, self._phi)
            if gcd != 1: 
                self.public_part = generate_random_number(2, self._phi)
            else:
                self.__private_part = (self._phi + d) % self._phi
                assert(self.__private_part>0)
                break
        
    

    @property
    def publickey(self):
        return RSAPublicKey(public_part = self.public_part, modulus = self.modulus)

    def decrypt_number(self, message: int):
        return fast_power(abs(message), self.__private_part, self.modulus)

    def decrypt_string(self, message:int):
        encoded = self.decrypt_number(message)
        return base64zlibdecode(encoded)

    
#TODO нужно добавить определение encode-decode алгоритма из сообщения. Можно с помощью объекта шифра, как в ECDSA
    

class RSAPublicKey(BaseModel):
    public_part: int
    modulus: int
        

    def encrypt_number(self, message: int):
        return fast_power(abs(message), self.public_part, self.modulus)


    def encrypt_string(self, message:str):
        encoded = base64zlibencode(message)
        return self.encrypt_number(encoded)
    
    def __str__(self):
        return f"RSAPublicKey(public_part={self.public_part}, modulus={self.modulus})"