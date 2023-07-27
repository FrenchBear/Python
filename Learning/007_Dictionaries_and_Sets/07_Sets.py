# Sets
# Learning Python
#
# Behind the scene sets are supported by dicts
#
# 2018-09-11    PV

# Just for fun
Ø:set = set()

s1 = set("précautionneusement")
s2 = set("applaudissements")
s3 = set("prestidigitateur")

print('s1:', s1)
print('s2:', s2)
print('s3:', s3)

print('s1 ∩ S2 ∩ S3:', s1.intersection(s2).intersection(s3))
print('s1 U S2 U S3:', s1.union(s2).union(s3))

i = s1.intersection(s2)
o = s1.symmetric_difference(s2)
assert i.isdisjoint(o)
assert i.union(o) == s1.union(s2)


# frozensets
f = frozenset("apple")
print(f)
g = frozenset(['p', 'a', 'l', 'e'])
print(g)
print(f.__hash__==g.__hash__)
