# Example 14-1. Our __setitem__ override is ignored by the __init__ and __update__ methods of the built-in dict

>>> class DoppelDict(dict):
...     def __setitem__(self, key, value):
...         super().__setitem__(key, [value] * 2)
...
>>> dd = DoppelDict(one=1)
>>> dd
{'one': 1}
>>> dd['two'] = 2
>>> dd
{'one': 1, 'two': [2, 2]}
>>> dd.update(three=3)
>>> dd
{'three': 3, 'one': 1, 'two': [2, 2]}
