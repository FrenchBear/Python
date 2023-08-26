# Example 12-7. Tests of enhanced Vector.__getitem__ from Example 12-6

>>> v7 = Vector(range(7))
>>> v7[-1]
6.0
>>> v7[1:4]
Vector([1.0, 2.0, 3.0])
>>> v7[-1:]
Vector([6.0])
>>> v7[1,2]
Traceback (most recent call last):
  ...
TypeError: 'tuple' object cannot be interpreted as an integer
