from ..Random import generate_random_number, generate_random_prime_number
from ..Math import fast_power, extended_euclidean_algorithm
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

    def decrypt_string_sample(self, message: str):
        '''
            Является sample-методом. Ужасно работает
            Для переработки надо построить хеш-функцию
        '''
        symbols = message.split(" ")
        string = ""
        for symbol in symbols:
            try:
                string += chr(self.decrypt_number(int(symbol)))
            except ValueError:
                raise Exception(f"Can't decrypt. Message has wrong symbols: {symbol}")
        return string
    
    
    

class RSAPublicKey(BaseModel):
    public_part: int
    modulus: int
        

    def encrypt_number(self, message: int):
        return fast_power(abs(message), self.public_part, self.modulus)


    def encrypt_string_sample(self, message: str):
        '''
            Является sample-методом. Ужасно работает
            Для переработки надо построить хеш-функцию
        '''
        symbols = []
        for symbol in message:
            symbol_order = ord(symbol)
            symbols.append(str(self.encrypt_number(symbol_order)))
        return " ".join(symbols)