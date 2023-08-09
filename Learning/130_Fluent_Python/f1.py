# Doctest of a string

import os       # noqa: F401
import doctest


s = """
>>> import collections
>>> class DoppelDict2(collections.UserDict):
...     def __setitem__(self, key, value):
...         super().__setitem__(key, [value] * 2)
...
>>> dd = DoppelDict2(one=1)
>>> dd
{'one': [1, 1]}
>>> dd['two'] = 2
>>> dd
{'two': [2, 2], 'one': [1, 1]}
>>> dd.update(three=3)
>>> dd
{'two': [2, 2], 'three': [3, 3], 'one': [1, 1]}
>>> class AnswerDict2(collections.UserDict):
...     def __getitem__(self, key):
...         return 42
...
>>> ad = AnswerDict2(a='foo')
>>> ad['a']
42
>>> d = {}
>>> d.update(ad)
>>> d['a']
42
>>> d
{'a': 42}

"""

filename = r"C:\Development\GitHub\Python\Learning\130_Fluent_Python\f0.py"
with open(filename, "w", encoding="UTF-8") as fi:
   fi.write(s)
res = doctest.testfile(filename, report=False)

print("OK!" if res.failed == 0 else "**** ERRORS!")
