# FactWheel
# Computes factorization wheel efficiency
# 2016-08-07 PV

import functools

def ComputeEfficiency(l):
    # Computes products of elements in a list, that is, the number of elements of a block compressed using factorization wheel
    prod = functools.reduce(lambda x,y: x * y, l)
    # We need 1 bit per element of the block before compression
    fl = range(prod)
    # Eliminate in the block all multiples of elements in the list
    for i in l:
        fl = list(filter(lambda x: x % i != 0, fl))
    # Compute efficiency, 26.67% for [2, 3, 5] = 8 (number of bits to store 30 elements skipping multiples of 2, 3 and 5) / 30 (2*3*5 = number of elements in the block)
    print(l, prod, "->", len(fl), len(fl)/prod)


ComputeEfficiency([2])
ComputeEfficiency([2,3])
ComputeEfficiency([2,3,5])
ComputeEfficiency([2,3,5,7])
ComputeEfficiency([2,3,5,7,11])
ComputeEfficiency([2,3,5,7,11,13])
