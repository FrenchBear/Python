# deco.py
# Exercices on decorators
#
# 2018-09-03    PV
# 2018-09-07    PV      Variant with a class


import functools

def uppercase(func):
    @functools.wraps(func)                  # Preserve __name__ and __doc__ of original function in the decorated version
    def wrapper(*args, **kwargs):
        original_result = func(*args, **kwargs)
        modified_result = original_result.upper()
        return modified_result
    return wrapper

def strong(func):
    def wrapper():
        return '<strong>' + func() + '</strong>'
    return wrapper

def emphasis(func):
    def wrapper():
        return '<em>' + func() + '</em>'
    return wrapper


@strong
@emphasis
@uppercase
def greet():
    return 'Hello!'

print(greet())

@uppercase
def hello(name:str) -> str:
    """This is a polite function to say hello"""
    return 'Hello '+name+'!'

print(hello('Pierre'))
print("name:", hello.__name__)
print("doc:", hello.__doc__)

def trace(func):
    def wrapper(*args, **kwargs):
        print(f'TRACE: calling {func.__name__}() with {args}, {kwargs}')
        original_result = func(*args, **kwargs)
        print(f'TRACE: {func.__name__}() returned {original_result!r}')
        return original_result
    return wrapper

@trace
def say(name, line):
    return f'{name}: {line}'

print(say('Jane', 'Hello, World'))



# Variant, with a class
# While a function embedded in a function gets a closer with outer function parameters, there is
# no such thing here, and self.original is a "manual closure"

class SkipLines():
    def __init__(self, n):
        self.n = n
        self.original = None

    def register(self, f):
        self.original = f
        return self.relay
    
    def relay(self, *args, **kwargs):
        for _ in range(self.n):
            print('-'*20)
        self.original(*args, **kwargs)
        for _ in range(self.n):
            print('-'*20)

    __call__ = register


@SkipLines(2)
def PrintHello(n):
    print("Hello,", n)

PrintHello("Pierre")

