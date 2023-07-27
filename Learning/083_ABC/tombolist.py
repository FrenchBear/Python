# tobolist is a class implementing Tombola interface and inheriting from list, but using virtual inheritance
# 2021-04-28    PV

from random import randrange
from tombola import Tombola

@Tombola.register               # class registered as a virtual subclass of Tombola
class TomboList(list):
    def pick(self):
        if (self):
            return self.pop(randrange(len(self)))
        raise LookupError('pop from empty ToboList')
    
    load = list.extend

    def loaded(self):
        return bool(self)       # Can't use trick of previous line since list does not implement __bool__

    def inspect(self):
        return tuple(sorted(self))


if __name__=='__main__':
    tl = TomboList()
    print(issubclass(TomboList, Tombola))
    print(isinstance(tl, Tombola))
    print(TomboList.__mro__)        # No fallback on Tombola since TomboList doesn't inherit from Tombola
