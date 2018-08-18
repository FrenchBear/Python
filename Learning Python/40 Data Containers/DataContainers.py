# DataContainers.py
# Examples of Python data structures
#
# 2018-08-17    PV

# List: mutable, any type
l = [1, 2, 3.1416, True, "Yes"]
print(type(l), l)

# Tuple: immutable, any type
t = (1, 2, 3.1416, True, "Yes")
print(type(t), t)

# Set
s = {1, 2, 3.1416, True, "Yes"}
print(type(s), s)

# Dictionary
d = {"un": 1, "deux": 2, "π": 3.1416, "vrai": True, "oui": "Yes"}
print(type(d), d)

# Named tuple
from collections import namedtuple
NTDemo = namedtuple("NTDemo", "int1 int2 decimal booleen ouinon")
nt = NTDemo(1, 2, 3.1416, True, "Yes")
print(type(nt), nt)

# Python array, behaves like a list but more efficient, can only contain one type.
# a*2 returns an array of twice the length, two copies of a appended (it's not a numpy array!)
from array import array
a = array('I', [0, 1, 1, 2, 3, 5, 8, 13])
print(type(a), a)

