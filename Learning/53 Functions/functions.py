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

def myfunc(a:int, b, c:str='hello', d:bool=true, *args, z=None, **kwargs):
    # l =len(args)+len(kwargs)
    print('a:', a, ' b:', b, ' c:', c, ' d:', d, ' z:', z, ' args:', args, ' kwarks:', kwargs, sep='')

myfunc(3, [1, 2])
myfunc(0, 1, 'world', False, z=12, myckey='mouse')
myfunc(0, 1, '2', True, 4, 5, six=6, sept=7, z='zero')

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
print()
print(str(sig))     # (a, b, c='hello', d=True, *args, z=None, **kwargs)
for name, param in sig.parameters.items():
    print(param.kind, ':', name, '=', param.default)
# POSITIONAL_OR_KEYWORD : a = <class 'inspect._empty'>
# POSITIONAL_OR_KEYWORD : b = <class 'inspect._empty'>
# POSITIONAL_OR_KEYWORD : c = hello
# POSITIONAL_OR_KEYWORD : d = True
# VAR_POSITIONAL : args = <class 'inspect._empty'>
# KEYWORD_ONLY : z = None
# VAR_KEYWORD : kwargs = <class 'inspect._empty'>

# divmod has positional parameters only (can't use names), only accessible to functions implemented in C
print()
sigdm = signature(divmod)
print(str(sigdm))     # (x, y, /)
for name, param in sigdm.parameters.items():
    print(param.kind, ':', name, '=', param.default)
# POSITIONAL_ONLY : x = <class 'inspect._empty'>
# POSITIONAL_ONLY : y = <class 'inspect._empty'>


# bind applies standard python matching rules
print()
bound_args = sig.bind(0, 1, '2', True, 4, 5, six=6, sept=7, z='zero')
for name, value in bound_args.arguments.items():    # bound_args.arguments is an OrderedDict
    print(name, '=', value)
# a = 0
# b = 1
# c = 2
# d = 3
# args = (4, 5)
# z = zero
# kwargs = {'six': 6, 'sept': 7}    

