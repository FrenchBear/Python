# Tuples
# Learning Python
#
# 2015-05-02    PV
# 2018-09-09    PV      Added namedtuple, NamedTuple, @dataclass


from dataclasses import dataclass
from typing import NamedTuple
from collections import namedtuple
t = 1, 2, 3
u = (4, 5, 6)

print(t)
print(t[0])

print(u)

# Tuples are immutable
# t[0]=2     # TypeError: 'tuple' object does not support item assignment

# Tuple concatenation, similar to lists and strings
print(t+u)

# Multiple assignation using tuples
a, b, c = t
# a,b=t     # ValueError: too many values to unpack (expected 2)
d, e = 10, 11

# Return multiple values
def min_max(list):
    list.sort()
    return list[0], list[-1]    # Negative index start from end


l = [5, 1, 2, 4, 7, 5, 9, 6, 2, 3, 5, 4, 6, 2, 4]
print(l)
min, max = min_max(l)
print(min, max)
print(l)                # l has been globally sorted


# Python old school, Immutable namedtuple
Car = namedtuple('Car', 'Brand Color Year')
c1 = Car(Brand='Renault', Color='White', Year=2016)
print(c1, c1.Brand)
# c1.Brand = 'Jaguar'       # AttributeError: can't set attribute


# Python 3.6 -- Typed declaration of namedtuple, inheriting from NamedTuple.  Immutable
class Voiture(NamedTuple):
    Brand: str
    Color: str
    Year: int


v1 = Voiture(Brand='Peugeot', Color='Gris', Year=2013)
print(v1, v1.Brand)
# v1.Brand = 'Jaguar'        # AttributeError: can't set attribute


# Python 3.7 -- Mutable class
@dataclass
class Bagnole:
    Brand: str
    Color: str
    Year: int


b1 = Bagnole(Brand='Mercedes', Color='Noir', Year=2017)
print(b1, b1.Brand)
b1.Brand = 'Jaguar'
print(b1)
