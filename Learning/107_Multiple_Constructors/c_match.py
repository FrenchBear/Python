# Play with Python contructors
# 03 checking argument types: example of multiple constructors based on arguments analysis
# This time using match of Python 3.10
#
# 2022-03-19    PV
# 2022-04-16    PV      Added exceptions in init_float for math.nan and math.inf

import numbers
import fractions
import math


class Fract:
    num: int
    den: int
    __match_args__ = ('num', 'den')     # For matching with deconstruction (see testmatch.py)

    # Construct a fraction from:
    # ()        -> zero
    # (int)     -> numerator
    # (int,int) -> num/den
    # (float)   -> Stern-Brocot algorithm to transform a periodic decimal suite into a fraction
    # (Fract)   -> copy constructor
    # (fraction)-> copy of the fraction in a Fract

    def __init__(self, numerator=None, denominator=None):
        if numerator is None and denominator is not None:
            raise ValueError('Can\'t define denumerator without defining numerator')

        if numerator is None:
            self.num = 0
            self.den = 1
            return

        if isinstance(numerator,  numbers.Integral):
            if denominator is not None and not isinstance(denominator,  numbers.Integral):
                raise TypeError('Numerator must be integer')
            self.init_int(int(numerator), 1 if denominator is None else int(denominator))
            return

        if denominator is not None:
            raise ValueError('Can\'t define denominator if numerator is not integer')

        # Use match pattern of Python 3.10
        match numerator:
            case float(f1):
                self.init_float(f1)
            # case Fract(n, d):             # Example with deconstruction
            #     self.init_int(n, d)
            case Fract():                   # Example without deconstruction
                self.init_fract(numerator)
            case fractions.Fraction():      # Does not support deconstruction, juct check type.  Must use parentheses
                self.init_fraction(numerator)
            case _:
                raise TypeError('Unsupported Fract init value')


    def init_int(self, numerator: int, denominator: int):
        if denominator == 0:
            raise ZeroDivisionError('Denominator can\'t be 0')
        self.num = numerator
        self.den = 1 if denominator is None else denominator
        self.normalize()

    def init_fract(self, f: 'Fract'):
        self.num = f.numerator
        self.den = f.denominator

    def init_fraction(self, f: fractions.Fraction):
        self.num = f.numerator
        self.den = f.denominator

    # Stern-Brocot algorithm to transform a periodic decimal suite into a fraction
    # Based on the fact that Stern-Brocot tree of fractions contains one and only once all fractions,
    def init_float(self, f: float):
        epsilon = 1e-6

        # Special float values are not supported
        if math.isnan(f):
            raise ValueError('Cannot convert NaN to integer ratio')
        if math.isinf(f):
            raise OverflowError('Cannot convert Infinity to integer ratio')

        # Special case
        if f == 0.0:
            self.num = 0
            self.den = 1
            return

        sign = 1
        if f < 0:
            sign = -1
            f = -f

        off = math.floor(f)
        f -= off
        if f <= epsilon:
            self.num = off * sign
            self.den = 1
            return

        infNum = 0; infDen = 1
        supNum = 1; supDen = 0
        while True:
            rNum = infNum + supNum
            rDen = infDen + supDen

            r = rNum / rDen
            if abs(r - f) < epsilon:
                self.num = (rNum + off * rDen) * sign
                self.den = rDen
                # No need for normalization, Stern-Brocot directly produces reduced fractions
                return

            if r < f:
                infNum = rNum
                infDen = rDen
            else:
                supNum = rNum
                supDen = rDen

    def normalize(self):
        # By convention, denominator is always >0
        if self.den < 0:
            self.num = -self.num
            self.den = -self.den
        # Only store reduced fractions
        if (p := math.gcd(self.num, self.den)) > 1:
            self.num //= p
            self.den //= p

    def __str__(self):
        if self.den == 1:
            return str(self.num)
        else:
            return str(self.num)+'/'+str(self.den)
    
    def __repr__(self):
        if self.den == 1:
            return f'Fract({self.num})'
        else:
            return f'Fract({self.num}, {self.den})'

    @property
    def numerator(self):
        return self.num

    @property
    def denominator(self):
        return self.den




# Python's library fractions.Fraction does not support (yet) match deconstruction
# Fraction is a derived class adding support for match deconstruction
class Fraction(fractions.Fraction):
    __match_args__ = ('numerator', 'denominator')


f3 = Fraction(4, 3)
match f3:
   case Fraction(n, d):
       print(f'Match Fraction: n={n}, d={d}')

match f3:
   case fractions.Fraction():
       print(f'Match fractions.Fraction: {f3!s} = {f3!r}')

print('__match_args__' in Fract.__dict__)
print('__match_args__' in fractions.Fraction.__dict__)
