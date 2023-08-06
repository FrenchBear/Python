# getitem_tuple_index.py
# Just try to implement a __getitem__ sich as [x][y] is the same as [x, y]
#
# 2023-08-06    PV

from collections import UserList

class MyList(UserList):
    def __getitem__(self, ix):
        if isinstance(ix, tuple):
            if len(ix)==1:
                return UserList.__getitem__(self, ix[0])
            else:
                return UserList.__getitem__(self, ix[0])[ix[1:]]
        print('my_index', ix)
        return UserList.__getitem__(self, ix)

ml3 = MyList((MyList((1,2,3)), MyList((4,5,6)), MyList((7,8,9))))
print(ml3[0][1])
print(ml3[0,1])
