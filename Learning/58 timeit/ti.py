# ti.py - Play with timeit
# Learning python
#
# From email of Dan at Real Python
#
# 2018-10-09	PV

import timeit

t = timeit.timeit('"-".join(str(n) for n in range(100))', number=10000)
print(t)

t = timeit.timeit('"-".join([str(n) for n in range(100)])', number=10000)
print(t)

t = timeit.timeit('"-".join(map(str, range(100)))', number=10000)
print(t)
