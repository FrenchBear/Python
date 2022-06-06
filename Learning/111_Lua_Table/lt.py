# Attempt to implement a Lua table in Python using __getattr__/__getattribute__/__setattr__
#
# 2022-06-06    PV

from typing import Any

# Table1 stores attributes in a private dict, not into class dict
# Uses __getattr__ and self.__dict__ to avoid infinite recursion
class Table1:
    def __init__(self, init_dict=None):
        if init_dict:
            self.__dict__['dic'] = dict(init_dict)
        else:
            self.__dict__['dic'] = {}

    """
    Called when an attribute lookup has not found the attribute in the usual places (i.e. it is not an instance attribute nor is it found in the class tree for self). 
    This method should return the (computed) attribute value or raise an AttributeError exception.
    Note that if the attribute is found through the normal mechanism, __getattr__() is not called. 
    (This is an intentional asymmetry between __getattr__() and __setattr__().) 
    This is done both for efficiency reasons and because otherwise __getattr__() would have no way to access other attributes of the instance.
    Note that at least for instance variables, you can fake total control by not inserting any values in the instance attribute dictionary 
    (but instead inserting them in another object). 
    See the __getattribute__() method below for a way to actually get total control in new-style classes.
    """
    def __getattr__(self, __name: str) -> Any:
        if __name in self.__dict__['dic']:
            return self.__dict__['dic'][__name]
        raise AttributeError(f'This instance of {self.__class__.__name__} does not contain an attribute {__name}')

    def __setattr__(self, __name: str, __value: Any) -> None:
        self.__dict__['dic'][__name] = __value


f1 = Table1({'n': 1, 'd': 3})
f1.f = 1/3
print(f1.n, '/', f1.d, '≈', f1.f)
try:
    print(f1.z)
except AttributeError as err:
    print("Error:", err)


# Table2 stores attributes in class dict and __getattr__, so it's pretty simple
class Table2:
    def __init__(self, init_dict=None):
        if init_dict:
            self.__dict__.update(init_dict)

    def __getattr__(self, __name: str) -> Any:
        # When __name is a valid attribute, this method is not called
        raise AttributeError(f'This instance of {self.__class__.__name__} does not contain an attribute {__name}')

    def __setattr__(self, __name: str, __value: Any) -> None:
        self.__dict__[__name] = __value


f2 = Table2({'n': 2, 'd': 3})
f2.f = 2/3
print(f2.n, '/', f2.d, '≈', f2.f)
try:
    print(f2.z)
except AttributeError as err:
    print("Error:", err)


# Table3 uses __getattribute__ which is always called.  Calling object.__getattribute__(self, name) to avoid infinite recursion
class Table3:
    def __init__(self, init_dict=None):
        if init_dict:
            #self.dic = dict(init_dict)
            object.__setattr__(self, 'dic', dict(init_dict))
        else:
            #self.dic = {}
            object.__setattr__(self, 'dic', {})

    """
    Called unconditionally to implement attribute accesses for instances of the class. 
    If the class also defines __getattr__(), the latter will not be called unless __getattribute__() either calls it explicitly or raises an AttributeError. 
    This method should return the (computed) attribute value or raise an AttributeError exception. 
    In order to avoid infinite recursion in this method, its implementation should always call the base class method with the same name
    to access any attributes it needs, for example, object.__getattribute__(self, name).    
    """
    def __getattr__(self, __name: str) -> Any:
        d = object.__getattribute__(self, 'dic')
        if __name in d:
            return d[__name]
        raise AttributeError(f'This instance of {self.__class__.__name__} does not contain an attribute {__name}')

    def __setattr__(self, __name: str, __value: Any) -> None:
        d = object.__getattribute__(self, 'dic')
        d[__name] = __value


f3 = Table3({'n': 4, 'd': 3})
f3.f = 4/3
print(f3.n, '/', f3.d, '≈', f3.f)
try:
    print(f3.z)
except AttributeError as err:
    print("Error:", err)
