# Implementation of a StringBuilder class
# Use array.array to be a bit more memory-efficient than list, but append is bad
# 2018-09-09    PV

import array
import sys

class StringBuilderA:
    def __init__(self, initvalue):
        self.a = array.array('u', initvalue)

    def __str__(self):
        return ''.join(self.a)

    def append(self, s):
        for c in s:
            self.a.append(c)

sba = StringBuilderA("Bon")
sba.append("jour")
print(str(sba))


class StringBuilderL:
    def __init__(self, initvalue):
        self.l = list(initvalue)

    def __str__(self):
        return ''.join(self.l)

    def append(self, s):
        self.l.extend(list(s))

sbl = StringBuilderL("Bon")
sbl.append("jour")
print(str(sbl))


print("sizeof sba:", sys.getsizeof(sba))
print("sizeof sbl:", sys.getsizeof(sbl))
print("sizeof sba.a:", sys.getsizeof(sba.a))
print("sizeof sbl.l:", sys.getsizeof(sbl.l))

a = array.array('u', "Once upon a time")
l = list("Once upon a time")
print("sizeof a:", sys.getsizeof(a))
print("sizeof l:", sys.getsizeof(l))
