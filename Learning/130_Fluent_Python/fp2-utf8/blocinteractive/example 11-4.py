# Example 11-4. Comparing behaviors of classmethod and staticmethod

>>> class Demo:
...     @classmethod
...     def klassmeth(*args):
...         return args
...     @staticmethod
...     def statmeth(*args):
...         return args
>>> Demo.klassmeth()
(<class '__main__.Demo'>,)
>>> Demo.klassmeth('spam')
(<class '__main__.Demo'>, 'spam')
>>> Demo.statmeth()
()
>>> Demo.statmeth('spam')
('spam',)
