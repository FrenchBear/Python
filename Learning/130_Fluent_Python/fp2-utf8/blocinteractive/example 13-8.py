# Example 13-8. A fake Tombola doesn’t go undetected

>>> from tombola import Tombola
>>> class Fake(Tombola):
...     def pick(self):
...         return 13
...
>>> Fake
<class '__main__.Fake'>
>>> f = Fake()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: Can't instantiate abstract class Fake with abstract method load
