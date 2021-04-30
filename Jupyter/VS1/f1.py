# f1.py
# Test of Jypyter extension of VSCode
# 2021-04-22    PV

import math

def cube(x: float) -> float:
    return x**3

if __name__=='__main__':
    for i in range(1,11):
        print(i, math.sqrt(i))
