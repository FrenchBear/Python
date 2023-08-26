# Example 24-15. metabunch/from3_6/bunch.py: MetaBunch metaclass and Bunch class

class MetaBunch(type):
    def __new__(meta_cls, cls_name, bases, cls_dict):
        defaults = {}

        def __init__(self, **kwargs):
            for name, default in defaults.items():
                setattr(self, name, kwargs.pop(name, default))
            if kwargs:
                extra = ', '.join(kwargs)
                raise AttributeError(f'No slots left for: {extra!r}')

        def __repr__(self):
            rep = ', '.join(f'{name}={value!r}'
                            for name, default in defaults.items()
                            if (value := getattr(self, name)) != default)
            return f'{cls_name}({rep})'
        new_dict = dict(__slots__=[], __init__=__init__, __repr__=__repr__)

        for name, value in cls_dict.items():
            if name.startswith('__') and name.endswith('__'):
                if name in new_dict:
                    raise AttributeError(f"Can't set {name!r} in {cls_name!r}")
                new_dict[name] = value
            else:
                new_dict['__slots__'].append(name)
                defaults[name] = value
        return super().__new__(meta_cls, cls_name, bases, new_dict)

class Bunch(metaclass=MetaBunch):
    pass
