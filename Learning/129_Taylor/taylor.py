# Taylor.py
# Play with Taylor function
# From Windows calculator C++ code, function _sinrat
#
# 2023-04-20    PV

import math


def sin_taylor(x: float):
    x2 = x*x
    j = 0
    this_term = x
    somme = x
    for j in range(1, 100):
        next_term = -this_term*x2/(2*j*(2*j+1))
        next_somme = somme+next_term
        if somme == next_somme:
            break
        somme = next_somme
        this_term = next_term
    return somme


print(sin_taylor(math.pi/4))
