# Example 22-4. explore0.py: turn a JSON dataset into a FrozenJSON holding nested FrozenJSON objects, lists, and simple types

from collections import abc

class FrozenJSON:
    """A read-only façade for navigating a JSON-like object using attribute notation"""

    def __init__(self, mapping):
        self.__data = dict(mapping)

    def __getattr__(self, name):
        try:
            return getattr(self.__data, name)
        except AttributeError:
            return FrozenJSON.build(self.__data[name])

    def __dir__(self):
        return self.__data.keys()

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj
