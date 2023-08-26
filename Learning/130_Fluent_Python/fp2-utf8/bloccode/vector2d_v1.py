# Example 11-3. Part of vector2d_v1.py: this snippet shows only the frombytes class method, added to the Vector2d definition in vector2d_v0.py (Example 11-2)

    @classmethod
    def frombytes(cls, octets):
        typecode = chr(octets[0])
        memv = memoryview(octets[1:]).cast(typecode)
        return cls(*memv)
