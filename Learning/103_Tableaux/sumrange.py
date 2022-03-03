# sumrange.py
# somme d'une plage en O(1) avec précalcul en O(n)
# Programmer efficacement chap 4
# Mon implémentation (pas dans le livre)
#
# 2022-05-25    PV

import random
import itertools

l = list(random.randint(-10,10) for _ in range(25))
print(l)

# Build cumulative sum array, by convention cs[0]=0
cs = [0]
for i in l:
    cs.append(cs[-1]+i)
print(cs)

# itertools.accumulate is shorted, but does not provide initial 0, need to add it to keep cs[j]-cs[i] calculation simple and quick
cs2 = list(itertools.accumulate(l))
cs2.insert(0, 0)
print(cs2)

# verify all sums
for i in range(len(l)):
    for j in range(i, len(l)):
        s1 = cs[j]-cs[i]
        s2 = sum(l[i:j])
        assert(s1==s2)
