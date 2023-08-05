from array import array
from collections import UserList

a = array('i', range(24))
print(a)

mv1 = memoryview(a)
print(mv1.tolist())
mv2 = mv1.cast('b').cast('i', [4, 6])
print(mv2.tolist())
mv3 = mv1.cast('b').cast('i', [2, 3, 4])
print(mv3.tolist())

l3 = mv3.tolist()
print(l3[1][2][3])

class MyList(UserList):
    def __getitem__(self, ix):
        print('my_index', ix)
        return list.__getitem__(self, ix)

ml3 = MyList(l3)
print(ml3[1][2][3])
