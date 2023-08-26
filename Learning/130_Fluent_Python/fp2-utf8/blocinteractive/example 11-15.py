# Example 11-15. The ColorPixel, another subclass of Pixel

>>> class ColorPixel(Pixel):
...     __slots__ = ('color',)
>>> cp = ColorPixel()
>>> cp.__dict__
Traceback (most recent call last):
  ...
AttributeError: 'ColorPixel' object has no attribute '__dict__'
>>> cp.x = 2
>>> cp.color = 'blue'
>>> cp.flavor = 'banana'
Traceback (most recent call last):
  ...
AttributeError: 'ColorPixel' object has no attribute 'flavor'
