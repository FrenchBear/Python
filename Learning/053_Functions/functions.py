# functions.py
# Learning Python - Functions as objects
# 
# 2018-09-24    PV
# 2018-10-04    PV      Detailed info and NewMath class


import dis
from inspect import signature
from collections.abc import Callable


def factorial(n: int = 0)->int:
    '''returns n!'''
    r = 1 if n < 2 else n * factorial(n-1)
    return r


print('42! =', factorial(42))

# Can add on-the-fly attributes to user-defined functions, into __dict__ member
factorial.author = "Pierre Violent"         # type: ignore[attr-defined]
factorial.datewritten = "2018-09-24"        # type: ignore[attr-defined]


def function_info(f):
    print('-----------------------------------------------')
    print('__name__:', f.__name__)
    print('__qualname__:', f.__qualname__)
    print('__doc__:', f.__doc__)
    print('__module__:', f.__module__)

    print('__dict__:', f.__dict__)

    print('__code__:', f.__code__)
    if True:
        print('__code__.co_argcount:', f.__code__.co_argcount)
        print('__code__.co_cellvars:', f.__code__.co_cellvars)
        print('__code__.co_code:', f.__code__.co_code)
        print('__code__.co_consts:', f.__code__.co_consts)
        print('__code__.co_filename:', f.__code__.co_filename)
        print('__code__.co_firstlineno:', f.__code__.co_firstlineno)
        print('__code__.co_flags:', f.__code__.co_flags)
        print('__code__.co_freevars:', f.__code__.co_freevars)
        print('__code__.co_kwonlyargcount:', f.__code__.co_kwonlyargcount)
        print('__code__.co_lnotab:', f.__code__.co_lnotab)
        print('__code__.co_name:', f.__code__.co_name)
        print('__code__.co_names:', f.__code__.co_names)
        print('__code__.co_nlocals:', f.__code__.co_nlocals)
        print('__code__.co_stacksize:', f.__code__.co_stacksize)
        print('__code__.co_varnames:', f.__code__.co_varnames)

    print('__defaults__:', f.__defaults__)

    print(dis.disassemble(f.__code__))

    print('__kwdefaults__:', f.__kwdefaults__)

    print('__annotations__:', f.__annotations__)
    print('__closure__:', f.__closure__)


function_info(factorial)


print('\n\n')


def myfunc(a: int, b, c: str = 'hello', d: bool = True, *args, z=None, **kwargs):
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

print('myfunc.__defaults__:', myfunc.__defaults__)      # type: ignore[attr-defined]
print('myfunc.__kwdefaults__:', myfunc.__kwdefaults__)  # type: ignore[attr-defined]
print('myfunc varnames:', myfunc.__code__.co_varnames)
print('myfunc argcount:', myfunc.__code__.co_argcount)


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


# ---------------------------------------------------------------------'
print('\n')



class NewMath:
    'Experimental Mathematics'

    def multiplier_builder(self, k: int = 1) -> Callable[[float], float]:
        'Returns a multiplier-by-k function'
        def multiplier(x: float)->float:
            'Implementation of actual multiplier of input parameter by free variable k'
            return k*x
        return multiplier


nm = NewMath()
f1 = nm.multiplier_builder
f2 = NewMath.multiplier_builder

# f1 is bound to nm objects and only needs 1 argument, while f2 is unbound and needs 2 arguments, with a NewMath object as 1st arg
# function_info generates the same output for f1,a nd f2 so at this stage, I don't know how to differentiate both versions using metainformation
# But signature sees the difference, reports 1 arg for f1 and 2 for f2

function_info(f1)

sig1 = signature(f1)
print()
print(str(sig1))
for name, param in sig1.parameters.items():
    print(param.kind, ':', name, '=', param.default)


function_info(f2)

sig2 = signature(f2)
print()
print(str(sig2))
for name, param in sig2.parameters.items():
    print(param.kind, ':', name, '=', param.default)

# Look for all __code__ members
# for k in dir(f1.__code__):
#     # if k.startswith('co_'):
#     print("print('"+k+":', f.__code__."+k+")")

