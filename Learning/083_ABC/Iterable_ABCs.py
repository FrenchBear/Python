# Iterable_ABCs.py
# Shows the specific members of some iterables
#
# 2023-08-04    PV

from abc import abstractmethod
from collections import abc
from typing import SupportsAbs, runtime_checkable, TypeVar, Protocol

class EmptyBase:
    pass

"""
print('\nIterable:')
print(set(dir(Iterable)) - set(dir(EmptyBase)))
print('\nCollecction:')
print(set(dir(Collection)) - set(dir(Iterable)))
print('\nSequence:')
print(set(dir(Sequence)) - set(dir(Collection)))
print('\nMutableSequence:')
print(set(dir(MutableSequence)) - set(dir(Sequence)))
print('\nList:')
print(set(dir(list)) - set(dir(MutableSequence)))
"""

class Base:
    mylist = ['red','green','blue']

class L1_Iterable(Base):
    def __iter__(self):
        return iter(self.mylist)
print(issubclass(L1_Iterable, abc.Iterable))


class L1_Container(Base):
    def __contains__(self, value):
        return value in self.mylist
print(issubclass(L1_Container, abc.Container))


class L1_Sized(Base):
    def __len__(self):
        return len(self.mylist)
print(issubclass(L1_Sized, abc.Sized))


class L2_Reversible(L1_Iterable):
    def __reversed__(self):
        return reversed(self.mylist)
print(issubclass(L2_Reversible, abc.Reversible))


class L2_Collection(L1_Iterable, L1_Container, L1_Sized):
    __slots__ = ()

    @classmethod
    def __subclasshook__(cls, C):
        pass
print(issubclass(L2_Collection, abc.Collection))


# From here, doesn't work anymore
# abc implementations doesn't contain _is_subclasshook that check for specific methods
#
# Can use abc.<Class>.register(MyClass), but then it's not automatic anymore, and MyClass
# can actually contain nothing and issubclass(MyClass, abc.<Class>) will still return True.
#
# Another option, implement class SupportsXXX(Protocol) that implement abstract methods describing
# what's expected for XXX, then isinstance(MyClass, SupportsXXX) will return True if MyClass
# implements what's required in SupportsXXX


class L3_Sequence(L2_Reversible, L2_Collection):
    def __getitem__(self, index):
        return self.mylist[index]
    def count(self, value):
        return self.mylist.count(value)
    def index(self, value, start=0, stop=None):
        return self.mylist.index(value)
    def __class_getitem__(self, index):
        pass
print(issubclass(L3_Sequence, abc.Sequence))
# issubclass is False, even though L3_Sequence implements all that is required for abc.Sequence
print(set(dir(L3_Sequence)) - set(dir(EmptyBase)))


class L3_Mapping(L1_Iterable, L1_Container, L1_Sized):
    # def __getitem__(self, key):
    #     return self.mylist[key]
    # def get(self, key, default=None):
    #     pass
    # def __contains__(self, key):
    #     return super().__contains__(key)
    # def keys(self):
    #     pass
    # def items(self):
    #     pass
    # def values(self):
         pass
abc.Mapping.register(L3_Mapping)
print(issubclass(L3_Mapping, abc.Mapping))

#T_co = TypeVar('T_co', covariant=True)  # Any type covariant containers.

@runtime_checkable
#class SupportsSequence(Protocol[T_co]):
class SupportsSequence(Protocol):
    """An ABC supporting Sequence"""
    @abstractmethod
    def __iter__(self):  pass
    @abstractmethod
    def __reversed__(self):  pass
    @abstractmethod
    def __contains__(self, key):  pass
    @abstractmethod
    def __len__(self, key):  pass
    @abstractmethod
    def __getitem__(self, index):
        pass
    @abstractmethod
    def count(self, value):
        pass
    @abstractmethod
    def index(self, value, start=0, stop=None):
        pass

print(isinstance(L3_Sequence, SupportsSequence))
