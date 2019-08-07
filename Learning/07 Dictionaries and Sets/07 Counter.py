# Counter
# Learning Python
#
# 2018-09-11    PV

from collections import Counter

c = Counter({'apple': 2, 'pear': 3, 'cherry': 1})
c.update({'cherry': 3, 'banana': 2})
c['orange'] += 1
c['apple'] -= 2
c['orange'] += 4
# c['cherry'] -= 1
c.subtract({'orange':1, 'cherry':2, 'kiwi':2})

print(c)
print(c.most_common())
