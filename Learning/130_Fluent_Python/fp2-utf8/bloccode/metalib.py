# Example 24-18. metalib.py: the MetaKlass

class MetaKlass(type):
    print('% MetaKlass body')

    @classmethod
    def __prepare__(meta_cls, cls_name, bases):
        args = (meta_cls, cls_name, bases)
        print(f'% MetaKlass.__prepare__{args!r}')
        return NosyDict()

    def __new__(meta_cls, cls_name, bases, cls_dict):
        args = (meta_cls, cls_name, bases, cls_dict)
        print(f'% MetaKlass.__new__{args!r}')
        def inner_2(self):
            print(f'% MetaKlass.__new__:inner_2({self!r})')

        cls = super().__new__(meta_cls, cls_name, bases, cls_dict.data)
        cls.method_c = inner_2
        return cls

    def __repr__(cls):
        cls_name = cls.__name__
        return f"<class {cls_name!r} built by MetaKlass>"

print('% metalib module end')
