# Example 11-13. The Pixel class uses __slots__

>>> class Pixel:
...     __slots__ = ('x', 'y')
...
>>> p = Pixel()
>>> p.__dict__
Traceback (most recent call last):
  ...
AttributeError: 'Pixel' object has no attribute '__dict__'
>>> p.x = 10
>>> p.y = 20
>>> p.color = 'red'
Traceback (most recent call last):
  ...
AttributeError: 'Pixel' object has no attribute 'color'
