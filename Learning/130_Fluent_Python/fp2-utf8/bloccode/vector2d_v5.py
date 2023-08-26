# Example 13-17. vector2d_v5.py: adding annotations to the methods under study

    def __abs__(self) -> float:
        return math.hypot(self.x, self.y)

    def __complex__(self) -> complex:
        return complex(self.x, self.y)

    @classmethod
    def fromcomplex(cls, datum: SupportsComplex) -> Vector2d:
        c = complex(datum)
        return cls(c.real, c.imag)
