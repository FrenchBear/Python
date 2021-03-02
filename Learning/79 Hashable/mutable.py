# mutable.py
# play with immutable hashable class
# 2021-03-02    PV

class Vect2D:
    def __init__(self, x, y) -> None:
        self.__x = x        # __ makes __x private (at least declaratively, the name is just decorated in dir())
        self.__y = y

    # Makes this a readonly accessor
    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __str__(self) -> str:
        return f"({self.__x}, {self.__y})"

    def __repr__(self) -> str:
        return f"Vect2D({repr(self.__x)}, {repr(self.__y)})"

    def __iter__(self):
        yield self.__x
        yield self.__y

    def __eq__(self, o: object) -> bool:
        return self.__x == o.__x and self.__y == o.__y

    def __hash__(self) -> int:
        return hash(self.__x) ^ hash(self.__y)

    def mutate(self):
        self.__x = self.__x + 12


v1 = Vect2D(3, 4)
v2 = Vect2D(4, 3)

print(v1, hash(v1))
print(v2, hash(v2))

v3 = Vect2D('a', (3.14, 1.732))
print(repr(v3), hash(v3))

d = {}
d[v1] = 'vect1'
v1.mutate()
# print(d[v1])        # fails, a hashable object should be immutable

# print(v1.__x)       # Error: 'Vect2D' object has no attribute '__x'
print(v1._Vect2D__x)  # Cheating...
v1._Vect2D__x = 7     # even worse cheating
print(v1)
