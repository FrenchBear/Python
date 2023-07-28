# Doctest of a string

import os
import doctest


s = """
>>> fruits = ['strawberry', 'fig', 'apple', 'cherry', 'raspberry', 'banana']
>>> sorted(fruits, key=lambda word: word[::-1])
['banana', 'apple', 'fig', 'raspberry', 'strawberry', 'cherry']

"""

filename = r"C:\Temp\p0.py"
with open(filename, "w", encoding="UTF-8") as fi:
    fi.write(s)
res = doctest.testfile(filename, report=False)

print("OK!" if res.failed == 0 else "**** ERRORS!")
os._exit(0)


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
