# functions.py
# Learning Python - Functions as objects
# 2018-09-24    PV

# Marre de true et false en majuscules!
false = False
true = True


def factorial(n: int = 0)->int:
    '''returns n!'''
    r=1 if n < 2 else n * factorial(n-1)
    return r


print('42! =', factorial(42))


factorial.author = "Pierre Violent"
factorial.datewritten = "2018-09-24"
print('__dict__:', factorial.__dict__)

print('__doc__:', factorial.__doc__)

print('__annotations__:', factorial.__annotations__)

print('__closure__:', factorial.__closure__)

print('__code__:', factorial.__code__)
print('varnames:', factorial.__code__.co_varnames)
print('argcount:', factorial.__code__.co_argcount)
import dis
print(dis.disassemble(factorial.__code__))

print('__defaults__:', factorial.__defaults__)
print('__kwdefaults__:', factorial.__kwdefaults__)

print('__name__:', factorial.__name__)
print('__qualname__:', factorial.__qualname__)


print('\n\n')

def myfunc(a, b, c='hello', d=true, *args, z=None, **kwargs):
    l =len(args)+len(kwargs)
    print('a:', a, ' b:', b, ' c:', c, ' d:', d, ' z:', z, ' args:', args, ' kwarks:', kwargs, sep='')

myfunc(3.14, [1, 2])
myfunc(0, 1, 'world', False, z=12, myckey='mouse')
myfunc(0, 1, 2, 3, 4, 5, six=6, sept=7, z='zero')

# named parameters defined after *args arguments can only be given as keyword argument, it will never
# capture an unnamed positional argument.

# If you don’t want to support variable positional arguments but still want keyword-only arguments, put a * by itself in the signature, like this:
# b is keyword only, and mandatory (no default value)
def f(a, *, b):
    return a, b

print(f(1, b=2))
print(f('hello', b='word'))
# c=f(1,2)    # f() takes 1 positional argument but 2 were given
# c=f(1)      # f() missing 1 required keyword-only argument: 'b'

print('\n\n')

print('myfunc.__defaults__:', myfunc.__defaults__)
print('myfunc.__kwdefaults__:', myfunc.__kwdefaults__)
print('myfunc varnames:', myfunc.__code__.co_varnames)
print('myfunc argcount:', myfunc.__code__.co_argcount)

from inspect import signature
sig = signature(myfunc)
print(str(sig))
for name, param in sig.parameters.items():
    print(param.kind, ':', name, '=', param.default)
    