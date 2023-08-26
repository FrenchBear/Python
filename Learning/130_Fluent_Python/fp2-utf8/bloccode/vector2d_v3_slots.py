# Example 11-16. vector2d_v3_slots.py: the __slots__ attribute is the only addition to Vector2d

class Vector2d:
    __match_args__ = ('x', 'y')
    __slots__ = ('__x', '__y')

    typecode = 'd'
    # methods are the same as previous version
