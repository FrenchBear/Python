# Learning Python
# Sets
# Same project number 07 than dicts, since behind the scene sets are supported by dicts
#
# 2018-09-11    PV

s1 = set("précautionneusement")
s2 = set("applaudissements")
s3 = set("prestidigitateur")

print(s1)
print(s2)
print(s3)

print(s1.intersection(s2).intersection(s3))
print(s1.union(s2).union(s3))

i = s1.intersection(s2)
o = s1.symmetric_difference(s2)
assert i.isdisjoint(o)
assert i.union(o) == s1.union(s2)

