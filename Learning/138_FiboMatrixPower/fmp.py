# fmp.py
# Fibonacci calculation using matrix power
# https://www.threads.net/@iamragavhari/post/C_YpvTEBaCN/
#
# 2024-09-02    PV

import numpy as np

def matrix_power(matrix, power):
    result = np.identity(len(matrix), dtype=object)
    base = matrix

    while power:
        s = f"P={power}  B={base}  R={result}".replace("\n", " ")
        print(s)
        if power % 2:
            result = np.dot(result, base)
        if power!=1:
            base = np.dot(base, base)   # useless step in the last loop
        power //= 2

    print(f"R = {result}".replace("\n", " "))
    return result

def fibo(n: int) -> int:
    if n == 0:
        return 0
    if n == 1:
        return 1

    F = np.array([[1, 1], [1, 0]], dtype=object)
    result = matrix_power(F, n - 1)[0][0]
    return result

fibo(9)
# for i in range(1, 11):
#     f = fibo(i)
#     print(f"F{i} = {f}")
