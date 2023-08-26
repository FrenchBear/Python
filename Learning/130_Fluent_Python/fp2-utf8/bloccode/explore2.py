# Example 22-6. explore2.py: using __new__ instead of build to construct new objects that may or may not be instances of FrozenJSON

from collections import abc
import keyword

class FrozenJSON:
    """A read-only façade for navigating a JSON-like object using attribute notation"""

    def __new__(cls, arg):
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self.__data = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self.__data[key] = value

    def __getattr__(self, name):
        try:
            return getattr(self.__data, name)
        except AttributeError:
            return FrozenJSON(self.__data[name])

    def __dir__(self):
        return self.__data.keys()
