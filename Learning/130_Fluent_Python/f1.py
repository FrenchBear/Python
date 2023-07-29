# Doctest of a string

import os       # noqa: F401
import doctest


s = """
>>> fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
>>> sorted(fruits, key=lambda word: word[::-1])
['banana', 'apple', 'fig', 'raspberry', 'strawberry', 'cherry']

"""

filename = r"C:\Development\GitHub\Python\Learning\130_Fluent_Python\f0.py"
#with open(filename, "w", encoding="UTF-8") as fi:
#    fi.write(s)
res = doctest.testfile(filename, report=False)

print("OK!" if res.failed == 0 else "**** ERRORS!")
