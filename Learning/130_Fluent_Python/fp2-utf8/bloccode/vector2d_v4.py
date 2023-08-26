# Example 13-16. vector2d_v4.py: methods for converting to and from complex

    def __complex__(self):
        return complex(self.x, self.y)

    @classmethod
    def fromcomplex(cls, datum):
        return cls(datum.real, datum.imag)
