# Lost Lands 4
# Ferry puzzle
# 2020-09-08    PV

# Permutations already implemented in itertools, ready to use
import itertools
from collections import deque
from typing import Deque

p0 = deque([1,0,0,0,1,1,0,0])
p1 = deque([1,0,0,1,0,0,0,0])
p2 = deque([1,0,1,1,0,0,0,0])
p3 = deque([1,0,0,1,0,1,0,0])
p4 = deque([1,1,0,0,0,0,0,0])
p5 = deque([1,0,1,0,1,0,0,0])
p6 = deque([1,0,0,1,1,0,0,0])
p7 = deque([1,0,0,1,1,0,0,0])
p8 = deque([1,0,1,0,0,0,0,0])

allp = [p0,p1,p2,p3,p4,p5,p6,p7,p8]

# print(p0)
# p0.pop()
# p0.appendleft(0)
# print(p0)

# q0 = deque(p0)
# q0[1]=7
# print(q0)

ip = 0

def getband8(p:Deque[Deque[int]]) -> bool:
    res = deque(p.popleft())
    while True:
        off=0
        while off<8:
            if res[off]==0: break
            off+=1
        if off==8: return True
        q = deque(p.popleft())
        j = 8-off
        while j<8:
            if q[j]==1: return False
            j+=1
        q.rotate(off)
        for k in range(8):
            res[k] += q[k]
            if res[k]>1: return False


for p in itertools.permutations(allp):
    pp = deque(p)
    ip = 0
    #for b in range(3):
    if getband8(pp) and getband8(pp) and getband8(pp):
        print(p)
        pass

