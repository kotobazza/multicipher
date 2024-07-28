from pydantic import BaseModel
from typing import Optional

class EllipticCurve(BaseModel):
    """ Датакласс для элиптической кривой в форме y^2 = x^3 + ax + b над полем F_p. """
    
    a: int
    b: int
    p: int
    _d: int
    
    def __str__(self):
        return f"EllipticCurve(a={self.a}, b={self.b}, p={self.p})"



class EllipticCurvePoint(BaseModel):
    """ Класс для представления точек на элиптической кривой. """
    x: Optional[int]
    y: Optional[int]
    curve: EllipticCurve

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y) and self.curve == other.curve

    def __neg__(self):
        return Point(self.x, -self.y % self.curve.p, self.curve)

    def __add__(self, other):
        if self.x is None or self.y is None:
            return other
        if other.x is None or other.y is None:
            return self

        assert self.curve == other.curve

        # Случай, когда точки равны
        if self == other:
            if self.y == 0:
                return EllipticCurvePoint(x=None, y=None, curve=self.curve)
            # Удвоение точки
            s = (3 * self.x**2 + self.curve.a) * pow(2 * self.y, -1, self.curve.p)
            
        else:
            if self.x == other.x:
                return Point(None, None, self.curve)
            # Сложение различных точек
            s = (other.y - self.y) * pow(other.x - self.x, -1, self.curve.p)

        x_r = (s**2 - self.x - other.x) % self.curve.p
        y_r = (s * (self.x - x_r) - self.y) % self.curve.p

        return EllipticCurvePoint(x=x_r, y=y_r, curve=self.curve)

    def __rmul__(self, k):
        result = EllipticCurvePoint(x=None, y=None, curve=self.curve)
        addend = self

        while k:
            if k & 1:
                result += addend
            addend += addend
            k >>= 1

        return result

    def __str__(self):
        return f"EllipticCurvePoint(x={self.x}, y={self.y}, curve={self.curve.__repr__()})"