# Decimal period for inverts
# 2020-07-15    PV

import matplotlib.pyplot as plt

# https://oeis.org/A003592
# Numbers of the form 2^i*5^j with i, j >= 0.
from heapq import heappush, heappop

def A003592():
    pq = [1]
    seen = set(pq)
    while True:
        value = heappop(pq)
        yield value
        seen.remove(value)
        for x in 2*value, 5*value:
            if x not in seen:
                heappush(pq, x)
                seen.add(x)

sequence = A003592()
A003592_list = [next(sequence) for _ in range(100)]
#print(A003592_list)

def isA003592(n):
    global A003592_list
    return n in A003592_list

# https://oeis.org/A051626
# Period of decimal representation of 1/n, or 0 if 1/n terminates.
def A051626(n):
    if isA003592(n):
        return 0
    else:
        lpow=1
        while True:
            for mpow in range(lpow-1, -1, -1):
                if (10**lpow-10**mpow) % n == 0:
                    return lpow-mpow
            lpow += 1

x=range(1,1000)
y=list(map(A051626, x))

plt.scatter(x,y,marker='.')
plt.show()

