# Iterable_ABCs.py
# Shows the specific members of some iterables
#
# 2023-08-04    PV

from abc import abstractmethod
from collections import abc
import inspect
from typing import TypeVar, runtime_checkable, Protocol

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

# Automatic recognition of ABC base classes only works for the simplest of them, see
# detailed info in L3_Sequence below

class Base:
    mylist = ['red', 'green', 'blue']

class L1_Iterable(Base):
    def __iter__(self):
        return iter(self.mylist)

print('issubclass(L1_Iterable, abc.Iterable):', issubclass(L1_Iterable, abc.Iterable))


class L1_Container(Base):
    def __contains__(self, value):
        return value in self.mylist


print('issubclass(L1_Container, abc.Container):', issubclass(L1_Container, abc.Container))


class L1_Sized(Base):
    def __len__(self):
        return len(self.mylist)


print('issubclass(L1_Sized, abc.Sized):', issubclass(L1_Sized, abc.Sized))


class L2_Reversible(L1_Iterable):
    def __reversed__(self):
        return reversed(self.mylist)


print('issubclass(L2_Reversible, abc.Reversible):', issubclass(L2_Reversible, abc.Reversible))


class L2_Collection(L1_Iterable, L1_Container, L1_Sized):
    pass


print('issubclass(L2_Collection, abc.Collection):', issubclass(L2_Collection, abc.Collection))
print()

# From here, doesn't work anymore
# abc implementations doesn't contain _is_subclasshook that check for specific methods.
# Actuelly, this is explained in https://docs.python.org/3/library/collections.abc.html#collections-abstract-base-classes
# in Footnote 1.
#
# Also in Fluent Python, after example 13-12:
# For example, mappings implement __len__, __getitem__, and __iter__, but they are rightly not considered
# subtypes of Sequence, because you can’t retrieve items using integer offsets or slices.
# That’s why the abc.Sequence class does not implement __subclasshook__.
#
# Solution 1:
# Use abc.<Class>.register(MyClass), but then it's not automatic anymore, and MyClass
# can actually contain nothing and issubclass(MyClass, abc.<Class>) will still return True.
#
# Solution 2:
# Implement class SupportsXXX(Protocol) that implement abstract methods describing
# what's expected for XXX, then isinstance(MyClass, SupportsXXX) will return True if MyClass
# implements what's required in SupportsXXX
#
# Solution 3:
# Check if required methods of XXX are present, either in the class itself, or in one of its
# parent classes
#
# Solution 4:
# Class inherits from abc.XXX, this will ensure that isinstance(MyClass, XXX) will return true.
# If any virtual method is not implemented when an instance is created (at run-time), Pythin will raise an error.

class L3_Sequence(L2_Reversible, L2_Collection):
    def __getitem__(self, index):
        return self.mylist[index]

    def count(self, value):
        return self.mylist.count(value)

    def index(self, value, start=0, stop=None):
        return self.mylist.index(value)


# Auto-detection of abc.Sequence doen't work out of the box
print('issubclass(L3_Sequence, abc.Sequence):', issubclass(L3_Sequence, abc.Sequence))
# issubclass is False, even though L3_Sequence implements all that is required for abc.Sequence
print(set(dir(L3_Sequence)) - set(dir(EmptyBase)))

# Solution 1:
abc.Sequence.register(L3_Sequence)
print('issubclass(L3_Sequence, abc.Sequence):', issubclass(L3_Sequence, abc.Sequence))

# Solution 2:
@runtime_checkable
class SupportsSequence(Protocol):
    """An ABC supporting Sequence"""
    @abstractmethod
    def __iter__(self): pass
    @abstractmethod
    def __reversed__(self): pass
    @abstractmethod
    def __contains__(self, key): pass
    @abstractmethod
    def __len__(self, key): pass

    @abstractmethod
    def __getitem__(self, index):
        pass

    @abstractmethod
    def count(self, value):
        pass

    @abstractmethod
    def index(self, value, start=0, stop=None):
        pass

print('issubclass(L3_Sequence, SupportsSequence):', issubclass(L3_Sequence, SupportsSequence))

TSequence = TypeVar('TSequence', bound=SupportsSequence)
def test_L3_Sequence(x: TSequence):
    print('len(x):', len(x))


# Here is the static checking version, but for some reason, mypy doesn't see or accept methods
# from base classes, and reject next line call
test_L3_Sequence(L3_Sequence())


# Solution 3:
def _check_methods(C, methods: abc.Iterable):
    for method in methods:
        for B in C.__mro__:
            if method in B.__dict__:
                if B.__dict__[method] is None:
                    return NotImplemented
                # it's Ok
                break
        else:
            # The 'for B in bc' did not return NotImplemented or exited using break fter finfing method
            return NotImplemented
        # Ok, method is implemented in a BC, continue checking next method in methods
    return True

# A one-liner
def _check_methodsV2(C, methods: abc.Iterable):
    return True if all(any(method in B.__dict__ and B.__dict__[method] is not None for B in C.__mro__) for method in methods) else NotImplemented

def issequence(x) -> bool:
    return _check_methodsV2(x if inspect.isclass(x) else x.__class__, ('__getitem__', '__len__'))

print('issequence(L3_Sequence):', issequence(L3_Sequence))


# Solution 4:
class L3_SequenceV2(L2_Reversible, L2_Collection, abc.Sequence):
    def __getitem__(self, index):
        return self.mylist[index]

    def count(self, value):
        return self.mylist.count(value)

    def index(self, value, start=0, stop=None):
        return self.mylist.index(value)

_ = L3_SequenceV2()     # Be sure that all virtual methors are implemented
print('issubclass(L3_SequenceV2, abc.Sequence):', issubclass(L3_SequenceV2, abc.Sequence))
