# fpc.py - Fragile base class problem
# How a minimal change in a base class that does not change its own behavior can break a derived class
# Because in python, class members are implicitly virtual
# Example translated from Java https://medium.com/@cscalfani/goodbye-object-oriented-programming-a59cda4c0e53
# See also https://dzone.com/articles/lamenting-the-death-of-object-oriented-programming
#
# 2018-09-27    PV


class Array:
    def __init__(self):
        self.a = []

    def append(self, o):
        self.a.append(o)

    def append_list(self, r):
        for item in r:
            # self.a.append(item)     # Returns a count of 7
            # Returns a count of 12 since it's implicitly virtual, correct when called on Array, but on ArrayCount will call ArrayCount.append
            self.append(item)

    def get(self):
        return self.a


class ArrayCount(Array):
    def __init__(self):
        super().__init__()
        self.count = 0

    def append(self, o):
        self.count += 1
        super().append(o)

    def append_list(self, r):
        self.count += len(r)
        super().append_list(r)


A = ArrayCount()
A.append(3)
A.append(True)
A.append_list([i*i for i in range(5)])
print(A.get(), A.count)
