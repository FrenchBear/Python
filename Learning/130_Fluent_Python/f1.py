# --follow-imports=skip

import os
import doctest


s = """
>>> from dataclasses import dataclass
>>> @dataclass
... class DemoDataClass:
...     a: int
...     b: float = 1.1
...     c = 'spam'
...
>>> DemoDataClass.__annotations__
{'a': <class 'int'>, 'b': <class 'float'>}
>>> DemoDataClass.__doc__
'DemoDataClass(a: int, b: float = 1.1)'
>>> DemoDataClass.a
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: type object 'DemoDataClass' has no attribute 'a'
>>> DemoDataClass.b
1.1
>>> DemoDataClass.c
'spam'
>>> dc = DemoDataClass(9)
>>> dc.a
9
>>> dc.b
1.1
>>> dc.c
'spam'
>>> dc.a = 10
>>> dc.b = 'oops'

"""

filename = r"C:\Temp\p0.py"
with open(filename, "w", encoding="UTF-8") as fi:
    fi.write(s)
res = doctest.testfile(filename, report=False)

if res.failed == 0:
    print("OK!")

os._exit(0)


# filename = r'C:\Temp\fp2\BlocInteractive-u8\Example 4-15.py'
# res = doctest.testfile(filename, report=False)


def get_files(source: str) -> list[str]:
    """Retourne juste les fichiers d'un dossier, noms.ext sans chemins"""
    _1, _2, files = next(os.walk(source))
    return files


folder = r"C:\Temp\fp2\BlocInteractive-u8"
for file in list(get_files(folder)):
    f = os.path.join(folder, file)
    print(
        f"\n------------------------------------------------------------------------\n{f}\n"
    )
    res = doctest.testfile(os.path.join(folder, file))
    if res.failed == 0:
        os.remove(f)
    else:
        os._exit(0)
