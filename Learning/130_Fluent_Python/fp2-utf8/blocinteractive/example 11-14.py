# Example 11-14. The OpenPixel is a subclass of Pixel

>>> class OpenPixel(Pixel):
...     pass
...
>>> op = OpenPixel()
>>> op.__dict__
{}
>>> op.x = 8
>>> op.__dict__
{}
>>> op.x
8
>>> op.color = 'green'
>>> op.__dict__
{'color': 'green'}
