# fusion.py
# fusion de listes triées
# Programmer efficacement chap 4
# Mon implémentation sans regarder cette du livre!
# 2022-05-25    PV

def fusion(l1: list[int], l2: list[int]) -> list[int]:
    f = []
    len1 = len(l1)
    len2 = len(l2)
    i1 = i2 = 0
    while i1 < len1 and i2 < len2:
        if l1[i1] <= l2[i2]:
            f.append(l1[i1])
            i1 += 1
        else:
            f.append(l2[i2])
            i2 += 1
    f.extend(l1[i1:])
    f.extend(l2[i2:])
    return f

# For verification
def is_sorted(l: list[int]) -> bool:
    return all(l[i-1]<=l[i] for i in range(1, len(l)))

# assert(is_sorted([1,2,2,3]))
# assert(not is_sorted([4,1,2]))
# assert(is_sorted([0]))
# assert(is_sorted([]))

l1 = list(i*5 for i in range(15))
l2 = list(i*7 for i in range(12))
print(l1)
print(l2)
f = fusion(l1, l2)
print(f)

assert(len(f) == len(l1)+len(l2))
assert(all(x in f for x in l1))
assert(all(x in f for x in l2))
assert(is_sorted(f))
