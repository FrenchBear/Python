# Example 24-11. builderlib.py: bottom of the module

class Descriptor:
    print('@ Descriptor body')

    def __init__(self):
        print(f'@ Descriptor.__init__({self!r})')

    def __set_name__(self, owner, name):
        args = (self, owner, name)
        print(f'@ Descriptor.__set_name__{args!r}')

    def __set__(self, instance, value):
        args = (self, instance, value)
        print(f'@ Descriptor.__set__{args!r}')

    def __repr__(self):
        return '<Descriptor instance>'

print('@ builderlib module end')
