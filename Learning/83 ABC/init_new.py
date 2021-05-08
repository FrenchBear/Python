# init_new.py
# Play with __init__ and __new__
# https://stackoverflow.com/questions/674304/why-is-init-always-called-after-new
# 2021-06-08    PV

# Use __new__ when you need to control the creation of a new instance.
# Use __init__ when you need to control initialization of a new instance.
# __new__ is the first step of instance creation. It's called first, and is responsible for returning a new instance of your class.
# In contrast, __init__ doesn't return anything; it's only responsible for initializing the instance after it's been created.
# In general, you shouldn't need to override __new__ unless you're subclassing an immutable type like str, int, unicode or tuple.

# Problem in class A, __init__ is always callled, even if __new__ returns an already initialized object...
# Solution in class B, only do initialization if object does not contain a _initialized property

from typing import Dict


class A(object):
    _dict: Dict[str, 'A'] = dict()

    def __new__(cls):
        if 'key' in A._dict:
            print("EXISTS")
            return A._dict['key']
        else:
            print("NEW")
            return super(A, cls).__new__(cls)

    def __init__(self):
        print("INIT")
        A._dict['key'] = self
        print()

a1 = A()
a2 = A()
a3 = A()


# Solution, add a _initialized property...
class B(object):
    _dict: Dict[str, 'B'] = dict()

    def __new__(cls):
        if 'key' in B._dict:
            print("EXISTS")
            return B._dict['key']
        else:
            print("NEW")
            return super(B, cls).__new__(cls)

    def __init__(self):
        if not '_initialized' in dir(self):
            self._initialized = True
            print("INIT")
            B._dict['key'] = self
        else:
            print("ALREADY INITIALIZED")
        print()

print('A Tests --------------------------------------')
a1 = A()
a2 = A()
a3 = A()

print('B Tests --------------------------------------')
b1 = B()
b2 = B()
b3 = B()
