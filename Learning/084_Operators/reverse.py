# reverse.py
# Play with forward/reverse operator overload in Python
# Check if reverse is called when both operands are the same type (answer: it's not)
# 2021-05-09    PV

class A:
    def __init__(self, x) -> None:
        self.x = x

    def __str__(self) -> str:
        return str(self.x)

    def __add__(self, other):
        print('A.__add__  other:', other.__class__.__name__)
        if isinstance(other, A):
            if self.x==0:
                return NotImplemented
            else:
                return A(self.x+other.x)
        else:
            return NotImplemented

    def __radd__(self, other):
        print('A.__radd__  other:', other.__class__.__name__)
        if isinstance(other, A):
            return A(self.x+other.x)
        else:
            return NotImplemented



class B:
    def __init__(self, x) -> None:
        self.x = x

    def __str__(self) -> str:
        return str(self.x)

    def __add__(self, other):
        print('B.__add__  other:', other.__class__.__name__)
        if isinstance(other, A) or isinstance(other, B):
            return B(self.x+other.x)
        else:
            return NotImplemented

    def __radd__(self, other):
        print('B.__radd__  other:', other.__class__.__name__)
        if isinstance(other, (A, B)):       # More compact synthax than 'or' in __add__
            return B(self.x+other.x)
        else:
            return NotImplemented



a0, a1, a2 = A(0), A(1), A(2)

a3 = a1+a2
print(a3)

# a4 = a0+a1      # A.__radd__ is not called: Exception: unsupported operand type(s) for +: 'A' and 'A'
# print(a4)

b = B(2)
a4 = a0+b         # B.__radd__ gets called here
print(a4)
