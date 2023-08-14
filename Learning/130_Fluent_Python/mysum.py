# mysum.py
# Personal exercice, how to implement and hint sum
#
# 2023-08-12    PV

from typing import TypeVar, Protocol, Iterable, overload

T = TypeVar('T')

class SupportsAdd(Protocol):
    def __add__(self: T, other: T) -> T: ...

TA = TypeVar('TA', bound=SupportsAdd)


@overload
def mysum(it: Iterable[TA], init: None=...) -> TA: ...

@overload
def mysum(it: Iterable[TA], init: TA=...) -> TA: ...

#def mysum(it: Iterable[TA], init:TA|None = None) -> TA|None:
def mysum(it, init=None):
    if init is not None:
        s = init
    else:
        # Can't implement default(TA) since TA is just a hint, an annotation, python engine can't use it
        # Solution: get class of 1st element of it, and intantiating the class with no arguments provides the default value
        try:
            myiter = iter(it)
            cls = next(myiter).__class__
            s = cls()
        except StopIteration:
            # it is an empty iterable, and no default value: returns None
            return None

    for item in it:
        s = s+item
    return s

# following type: ignore are for pylance that
print(mysum(range(1,11)))                                       
print(mysum(['a','b','c'], ''))                                 
print(mysum(['X','Y','Z']))                                     
print(mysum((['L1a', 'L1b'], ['L2a'], ['L3a','L3b','L3c'])))    
print(mysum([], 'Hello'))                                       
print(mysum([]))

# print(mysum((object(), object(), object())))                    
# Previous line can't work, object() does not support add. MyPy flags correctly the problem:
# mysum.py:49: error: Value of type variable "TA" of "mysum" cannot be "object"  [type-var]                                               
