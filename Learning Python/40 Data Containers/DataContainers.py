# DataContainers.py
# Examples of Python data containers structures
#
# 2018-08-17    PV

# List: mutable, any type
l = [1, 2, 3.1416, True, "Yes"]
print(type(l), l)
l.append(4)
l.extend([5, 6, 7])

# Tuple: immutable, any type
t = (1, 2, 3.1416, True, "Yes")
print(type(t), t)

# Named tuple
from collections import namedtuple
NTDemo = namedtuple("NTDemo", "int1 int2 decimal booleen ouinon")
nt = NTDemo(1, 2, 3.1416, True, "Yes")
print(type(nt), nt)
d = nt.decimal
# nt.ouinon = "Maybe"       # No, a named tuple is immutable

# Python array, behaves like a list but more efficient and lean (as a C array), can only contain one type.
# a*2 returns an array of twice the length, two copies of a appended (it's not a numpy array!)
from array import array
ai = array('I', [0, 1, 1, 2, 3, 5, 8, 13, 3000000000])  # I=unsigned int
print(type(ai), ai)
with open('int.bin', 'wb') as fp:
    ai.tofile(fp)
ai2 = array('i')    # i=signed int
with open('int.bin', 'rb') as fq:
    ai2.fromfile(fq, 9)
print(ai2)
ai2.byteswap()
print(ai2)

# memoryview
numbers = array('h', [-2, -1, 0, 1, 2])  # h=signed short
memv = memoryview(numbers)
memv_oct = memv.cast('B')  # B=unsigned byte
print(memv_oct.tolist())

# numpy arrays
import numpy as np
an = np.random.randint(0, 100, (2, 5))  # Default type is I
print(an)
print(an > 50)
print(np.max(an, axis=0))
print(np.sum(an, axis=1))

# dequeue
from collections import deque
dq = deque(range(5))
dq.rotate(3)
dq.extend([11, 22])
dq.extendleft([100, 200])
dq.append(3.14)
dq.appendleft(1.414)
print(type(dq), dq)
dq.pop()        # Remove and return last item
dq.popleft()    # Remove and return first item


#################################
# Dictionaries and Sets

# Set
s = {1, 2, 3.1416, True, "Yes"}
print(type(s), s)
s.add(4)
s.update({"p", "o", "m"})

# Dictionary
d = {"un": 1, "deux": 2, "π": 3.1416, "vrai": True, "oui": "Yes"}
print(type(d), d)
d["e"] = 2.71828
d.update({"r2": 1.414, "r3": 1.732})

