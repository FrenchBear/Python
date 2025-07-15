# doc_test.py
# Test this feature
#
# 2027-07-15    PV

import doctest

def pgdc(a, b):
    """Calcule le pgdc de deux entiers positifs
    Si nécessaire, les nombres passés sont convertis en entier.
    >>> pgdc(12, 8)
    3
    >>> pgdc("4", 2.4) # conversion en entier
    2
    >>> pgdc(12, -8)
    Traceback (most recent call last):
    ...
    ValueError: Les deux entiers doivent être positifs
    """
    a, b = int(a), int(b)
    if (a < 0 or b < 0):
        raise ValueError("Les deux entiers doivent être positifs")
    while a != b:
        if (a > b):
            a = a - b
        else:
            b = b - a
    return a

print(pgdc(48, 18))

# This will report an error, that's on purpose!
doctest.testmod(verbose=True)
