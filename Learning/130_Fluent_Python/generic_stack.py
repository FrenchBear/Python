# generic_stack.py
# Simple test of Generic
#
# 2023-08-14    PV

from typing import TypeVar, Generic
from collections import deque

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self.q = deque[T]()
        # self.q: deque[T] = deque()

    def Push(self, value: T):
        self.q.append(value)

    def Pop(self) -> T:
        return self.q.pop()

s1 = Stack[int]()
s1.Push(1)
s1.Push(2)
s1.Push(3)
print(s1.Pop())

s2 = Stack[str]()
s2.Push('A')
s2.Push('B')
s2.Push('C')
print(s2.Pop())


T1 = TypeVar('T1')
T2 = TypeVar('T2')

# One type for each item
class Pair2(Generic[T1, T2]):
    def __init__(self, v1: T1, v2: T2) -> None:
        # self.p = tuple[T1,T2]((v1, v2))
        self.p = (v1, v2)

    def Item1(self) -> T1:
        return self.p[0]

    def Item2(self) -> T2:
        return self.p[1]

# Both items of the same type
class Pair1(Generic[T]):
    def __init__(self, v1: T, v2: T) -> None:
        self.p = (v1, v2)

    def Item1(self) -> T:
        return self.p[0]

    def Item2(self) -> T:
        return self.p[1]

p1 = Pair1[int](2, 3)

p2 = Pair2[int, str](3, 'three')

