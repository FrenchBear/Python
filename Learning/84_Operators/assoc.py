# assoc.py
# Play with operator associativity in Python
# From overloadable operators, only ** has a right-to-left associativity:
# 2**3**4 == 2**(3**4)
# 2021-05-09    PV

class A:
    def __init__(self, x) -> None:
        self.x = x

    def __str__(self) -> str:
        return str(self.x)

    def __pow__(self, other):
        if isinstance(other, A):
            return A(self.x ** other.x)
        else:
            return NotImplemented

    def __xor__(self, other):
        if isinstance(other, A):
            return A(self.x ** other.x)
        else:
            return NotImplemented


a2, a3, a4 = A(2), A(3), A(4)
print(a2, a3, a4)

p = a2**a3**a4
print(p)    # 2**(3**4) == 2417851639229258349412352

q = a2^a3^a4
print(q)    # (2**3)**4 == 4096


