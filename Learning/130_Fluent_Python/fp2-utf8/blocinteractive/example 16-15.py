# Example 16-15. Same comparisons as Example 16-13: last result changed

>>> va = Vector([1.0, 2.0, 3.0])
>>> vb = Vector(range(1, 4))
>>> va == vb
True
>>> vc = Vector([1, 2])
>>> from vector2d_v3 import Vector2d
>>> v2d = Vector2d(1, 2)
>>> vc == v2d
True
>>> t3 = (1, 2, 3)
>>> va == t3
False
