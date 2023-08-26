# Example 8-7. Runtime errors and how Mypy could have helped

>>> from birds import *
>>> woody = Bird()
>>> alert(woody)
Traceback (most recent call last):
  ...
AttributeError: 'Bird' object has no attribute 'quack'
>>> alert_duck(woody)
Traceback (most recent call last):
  ...
AttributeError: 'Bird' object has no attribute 'quack'
>>> alert_bird(woody)
Traceback (most recent call last):
  ...
AttributeError: 'Bird' object has no attribute 'quack'
