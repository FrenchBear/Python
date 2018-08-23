# Pythin built-in functions
# Learning Python
# From https://docs.python.org/3/library/functions.html
# 2016-08-10    PV

import sys
import math
import cmath
from os import system

system('chcp 65001 >nul')
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)


def test_abs():
    """
    abs(x)

    Return the absolute value of a number. The argument may be an integer or a floating point number. If the argument is a complex number, 
    its magnitude is returned.
    """
    print('\ntest_abs()')
    i = -2
    f = -3.25
    c = complex(3, 4)
    print('\tabs({0}) = {1}'.format(i, abs(i)))
    print('\tabs({0}) = {1}'.format(f, abs(f)))
    print('\tabs({0}) = {1}'.format(c, abs(c)))


def test_all():
    """
    all(iterable)

    Return True if all elements of the iterable are true (or if the iterable is empty).
    """
    def allEquiv(iterable):
        for element in iterable:
            if not element:
                return False
        return True

    print('\ntest_all()')
    l1 = [0, 1, 2]
    l2 = (1, 2, 3)
    l3 = {False}
    print('\tall({0}) = {1}'.format(l1, all(l1)))
    print('\tall({0}) = {1}'.format(l2, all(l2)))
    print('\tall({0}) = {1}'.format(l3, all(l3)))
    print('\tall({0}) = {1}'.format(l3, allEquiv(l3)))


def test_any():
    """
    any(iterable)

    Return True if any element of the iterable is true. If the iterable is empty, return False.
    """
    def anyEquiv(iterable):
        for element in iterable:
            if element:
                return True
        return False

    print('\ntest_any()')
    l1 = [0, 1, 2]
    l2 = (1, 2, 3)
    l3 = {False}
    print('\tall({0}) = {1}'.format(l1, any(l1)))
    print('\tall({0}) = {1}'.format(l2, any(l2)))
    print('\tall({0}) = {1}'.format(l3, any(l3)))
    print('\tall({0}) = {1}'.format(l3, anyEquiv(l3)))


def test_ascii():
    """
    ascii(object)

    As repr(), return a string containing a printable representation of an object, but escape the non-ASCII characters in the string returned by repr()
    using ∖x, ∖u or ∖U escapes. This generates a string similar to that returned by repr() in Python 2.
    """
    print('\ntest_ascii()')
    print('\tascii({0}) = {1}'.format(48, ascii(48)))
    c = chr(7)
    print('\tascii({0}) = {1}'.format(c, ascii(c)))
    s = "Hello\nWorld \u263A\n"
    print('\tascii({0}) = {1}'.format(s, ascii(s)))
    j = complex(3, 4)
    print('\tascii({0}) = {1}'.format(j, ascii(j)))


def test_bin():
    """
    bin(x)

    Convert an integer number to a binary string. The result is a valid Python expression. If x is not a Python int object, it has to define
    an __index__() method that returns an integer.
    """
    print('\ntest_bin()')
    print('\tbin({0:x}) = {1}'.format(0xCAFE, bin(0xCAFE)))
    print('\tbin({0:x}) = {1}'.format(0xDEADBEEF, bin(0xDEADBEEF)))


def test_bool():
    """
    bool([x])

    Convert a value to a Boolean, using the standard truth testing procedure. If x is false or omitted, this returns False; otherwise it returns True.
    bool is also a class, which is a subclass of int. Class bool cannot be subclassed further. Its only instances are False and True.
    """
    print('\ntest_bool()')
    print('\tbool({0}) = {1}'.format(0, bool(0)))
    print('\tbool({0}) = {1}'.format(23, bool(23)))


def test_breakpoint():
    """
    breakpoint(*args, **kws)

    This function drops you into the debugger at the call site. Specifically, it calls sys.breakpointhook(), passing args and kws straight through.
    By default, sys.breakpointhook() calls pdb.set_trace() expecting no arguments. In this case, it is purely a convenience function
    so you don’t have to explicitly import pdb or type as much code to enter the debugger. However, sys.breakpointhook() can be set
    to some other function and breakpoint() will automatically call that, allowing you to drop into the debugger of choice.
    New in version 3.7.
    """
    print('\ntest_breakpoint()')
    # breakpoint()


def test_bytearray():
    """
    bytearray([source[, encoding[, errors]]])

    Return a new array of bytes. The bytearray type is a mutable sequence of integers in the range 0 <= x < 256. It has most of the usual methods
    of mutable sequences, described in Mutable Sequence Types, as well as most methods that the bytes type has, see Bytes and Byte Array Methods.

    The optional source parameter can be used to initialize the array in a few different ways:
        If it is a string, you must also give the encoding (and optionally, errors) parameters; bytearray() then converts the string to bytes using str.encode().
        If it is an integer, the array will have that size and will be initialized with null bytes.
        If it is an object conforming to the buffer interface, a read-only buffer of the object will be used to initialize the bytes array.
        If it is an iterable, it must be an iterable of integers in the range 0 <= x < 256, which are used as the initial contents of the array.
    Without an argument, an array of size 0 is created.
    """
    print('\ntest_bytearray()')
    print('\tascii  -> ', list(bytearray("CAFE", "ascii")))
    print('\tcp850  -> ', list(bytearray("Café", "cp850")))
    print('\tcp1252 -> ', list(bytearray("Café", "cp1252")))
    print('\tutf-8  -> ', list(bytearray("Café♫🐗", "utf-8")))

    ba16 = bytearray("Café♫🐗🧔🧔🏻", "utf-16")
    print('\tutf-16 -> ', list(ba16))
    m16 = memoryview(ba16).cast('H')
    print('\tm16 ->    ', [hex(c) for c in m16.tolist()])

    ba32 = bytearray("Café♫🐗🧔🧔🏻", "utf-32")
    print('\tutf-32 -> ', list(ba32))
    m32 = memoryview(ba32).cast('L')
    print('\tm32 ->    ', [hex(c) for c in m32.tolist()])


def test_bytes():
    """
    class bytes([source[, encoding[, errors]]])

    Return a new “bytes” object, which is an immutable sequence of integers in the range 0 <= x < 256. bytes is an immutable version of bytearray,
    it has the same non-mutating methods and the same indexing and slicing behavior.
    Accordingly, constructor arguments are interpreted as for bytearray().
    Bytes objects can also be created with literals, see String and Bytes literals.
    See also Binary Sequence Types — bytes, bytearray, memoryview, Bytes Objects, and Bytes and Bytearray Operations.
    """
    print('\ntest_bytes()')
    tb1 = bytes([0xCA, 0xFE])
    print(type(tb1), tb1)
    tb2 = b'Hello'
    print(type(tb2), tb2)


def test_callable():
    """
    callable(object)

    Return True if the object argument appears callable, False if not. If this returns true, it is still possible that a call fails,
    but if it is false, calling object will never succeed. Note that classes are callable (calling a class returns a new instance);
    instances are callable if their class has a __call__() method.
    """
    print('\ntest_callable()')
    print('callable(print): ', callable(print))
    print('callable(3.14): ', callable(3.14))


def test_chr():
    """
    chr(i)

    Return the string representing a character whose Unicode code point is the integer i. For example, chr(97) returns the string 'a',
    while chr(8364) returns the string '€'. This is the inverse of ord().
    The valid range for the argument is from 0 through 1,114,111 (0x10FFFF in base 16). ValueError will be raised if i is outside that range.
    """
    print('\ntest_chr()')
    for i in [0x41, 0xE9, 0x266B, 0x1D11E, 0x1F43B]:
        print("%5x" % i, "->", chr(i))


def test_compile():
    """
    compile(source, filename, mode, flags=0, dont_inherit=False, optimize=-1)

    Compile the source into a code or AST object. Code objects can be executed by exec() or eval(). source can either be a normal string,
    a byte string, or an AST object. Refer to the ast module documentation for information on how to work with AST objects.

    The filename argument should give the file from which the code was read; pass some recognizable value if it wasn’t read 
    from a file ('<string>' is commonly used).

    The mode argument specifies what kind of code must be compiled; it can be 'exec' if source consists of a sequence of statements,
    'eval' if it consists of a single expression, or 'single' if it consists of a single interactive statement (in the latter case, 
    expression statements that evaluate to something other than None will be printed).

    The optional arguments flags and dont_inherit control which future statements affect the compilation of source. If neither is present 
    (or both are zero) the code is compiled with those future statements that are in effect in the code that is calling compile(). 
    If the flags argument is given and dont_inherit is not (or is zero) then the future statements specified by the flags argument 
    are used in addition to those that would be used anyway. If dont_inherit is a non-zero integer then the flags argument is it – 
    the future statements in effect around the call to compile are ignored.

    Future statements are specified by bits which can be bitwise ORed together to specify multiple statements. The bitfield 
    required to specify a given feature can be found as the compiler_flag attribute on the _Feature instance in the __future__ module.

    The argument optimize specifies the optimization level of the compiler; the default value of -1 selects the optimization level
    of the interpreter as given by -O options. Explicit levels are 0 (no optimization; __debug__ is true), 1 (asserts are removed, 
    __debug__ is false) or 2 (docstrings are removed too).

    This function raises SyntaxError if the compiled source is invalid, and ValueError if the source contains null bytes.

    If you want to parse Python code into its AST representation, see ast.parse().

    Note
    When compiling a string with multi-line code in 'single' or 'eval' mode, input must be terminated by at least one newline character. 
    This is to facilitate detection of incomplete and complete statements in the code module.

    Warning
    It is possible to crash the Python interpreter with a sufficiently large/complex string when compiling to an AST object 
    due to stack depth limitations in Python’s AST compiler.

    Changed in version 3.2: Allowed use of Windows and Mac newlines. Also input in 'exec' mode does not have to end in a newline 
    anymore. Added the optimize parameter.
    Changed in version 3.5: Previously, TypeError was raised when null bytes were encountered in source.
    """
    print('\ntest_compile()')
    codeobj = compile('x = 2\nprint("X is", x)', '', 'exec')
    exec(codeobj)
    codeobj2 = compile('1+2*3**4', '', 'eval')
    print("n=", eval(codeobj2))


def test_complex():
    """
    class complex([real[, imag]])

    Return a complex number with the value real + imag*1j or convert a string or number to a complex number. If the first parameter is a string, 
    it will be interpreted as a complex number and the function must be called without a second parameter. The second parameter can never be a string. 
    Each argument may be any numeric type (including complex). If imag is omitted, it defaults to zero and the constructor serves as a numeric conversion 
    like int and float. If both arguments are omitted, returns 0j.

    Note
    When converting from a string, the string must not contain whitespace around the central + or - operator. 
    For example, complex('1+2j') is fine, but complex('1 + 2j') raises ValueError.

    The complex type is described in Numeric Types — int, float, complex.

    Changed in version 3.6: Grouping digits with underscores as in code literals is allowed.
    """
    print('\ntest_complex()')
    c1 = cmath.acos(2.0)
    c2 = complex(0, math.log(2+math.sqrt(3)))
    print("c1 = {:.6f}".format(c1), "  cos -> ", cmath.cos(c1))
    print("c2 = {:.6f}".format(c2), "  cos -> ", cmath.cos(c2))


def test_delattr():
    """
    delattr(object, name)

    This is a relative of setattr(). The arguments are an object and a string. The string must be the name of one of the object’s attributes.
    The function deletes the named attribute, provided the object allows it. For example, delattr(x, 'foobar') is equivalent to del x.foobar.
    """
    print('\ntest_delattr()')

    class MyComplex:
        real = 3.1416
        imag = 1.7321

        def __str__(self):
            return "".join(f"{k}={getattr(self, k)} " for k in dir(self) if not k.startswith("__"))

    tda = MyComplex()
    print(tda)
    delattr(MyComplex, "imag")
    print(tda)


def test_dict():
    """
    class dict(**kwarg)
    class dict(mapping, **kwarg)
    class dict(iterable, **kwarg)

    Create a new dictionary. The dict object is the dictionary class. See dict and Mapping Types — dict for documentation about this class.
    For other containers see the built-in list, set, and tuple classes, as well as the collections module.
    """
    print('\ntest_dict()')
    a = dict(one=1, two=2, three=3)
    b = {'one': 1, 'two': 2, 'three': 3}
    c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
    d = dict([('two', 2), ('one', 1), ('three', 3)])
    e = dict({'three': 3, 'one': 1, 'two': 2})
    # Note that comparison is on properties/values, not on object id
    print(a == b == c == d == e)


def test_dir():
    print('\ntest_dir()')


def test_divmod():
    print('\ntest_divmod()')


def test_enumerate():
    print('\ntest_enumerate()')


def test_eval():
    print('\ntest_eval()')


def test_exec():
    print('\ntest_exec()')


def test_filter():
    print('\ntest_filter()')


def test_float():
    print('\ntest_float()')


def test_format():
    print('\ntest_format()')


def test_frozenset():
    print('\ntest_frozenset()')


def test_getattr():
    print('\ntest_getattr()')


def test_globals():
    print('\ntest_globals()')


def test_hasattr():
    print('\ntest_hasattr()')


def test_hash():
    print('\ntest_hash()')


def test_help():
    print('\ntest_help()')


def test_hex():
    print('\ntest_hex()')


def test_id():
    print('\ntest_id()')


def test_input():
    print('\ntest_input()')


def test_int():
    print('\ntest_int()')


def test_isinstance():
    print('\ntest_isinstance()')


def test_issubclass():
    print('\ntest_issubclass()')


def test_iter():
    print('\ntest_iter()')


def test_len():
    print('\ntest_len()')


def test_list():
    print('\ntest_list()')


def test_locals():
    print('\ntest_locals()')


def test_map():
    print('\ntest_map()')


def test_max():
    print('\ntest_max()')


def test_memoryview():
    print('\ntest_memoryview()')


def test_min():
    print('\ntest_min()')


def test_next():
    print('\ntest_next()')


def test_object():
    print('\ntest_object()')


def test_oct():
    print('\ntest_oct()')


def test_open():
    print('\ntest_open()')


def test_ord():
    print('\ntest_ord()')


def test_pow():
    print('\ntest_pow()')


def test_print():
    print('\ntest_print()')


def test_property():
    print('\ntest_property()')


def test_range():
    print('\ntest_range()')


def test_repr():
    print('\ntest_repr()')


def test_reversed():
    print('\ntest_reversed()')


def test_round():
    print('\ntest_round()')


def test_set():
    print('\ntest_set()')


def test_setattr():
    print('\ntest_setattr()')


def test_slice():
    print('\ntest_slice()')


def test_sorted():
    print('\ntest_sorted()')


def test_str():
    print('\ntest_str()')


def test_sum():
    print('\ntest_sum()')


def test_super():
    print('\ntest_super()')


def test_tuple():
    print('\ntest_tuple()')


def test_type():
    print('\ntest_type()')


def test_vars():
    print('\ntest_vars()')


def test_zip():
    print('\ntest_zip()')


test_abs()
test_all()
test_any()
test_ascii()
test_bin()
test_bool()
test_breakpoint()
test_bytearray()
test_bytes()
test_callable()
test_chr()
test_compile()
test_complex()
test_delattr()
test_dict()
"""
test_dir()
test_divmod()
test_enumerate()
test_eval()
test_exec()
test_filter()
test_float()
test_format()
test_frozenset()
test_getattr()
test_globals()
test_hasattr()
test_hash()
test_help()
test_hex()
test_id()
test_input()
test_int()
test_isinstance()
test_issubclass()
test_iter()
test_len()
test_list()
test_locals()
test_map()
test_max()
test_memoryview()
test_min()
test_next()
test_object()
test_oct()
test_open()
test_ord()
test_pow()
test_print()
test_property()
test_range()
test_repr()
test_reversed()
test_round()
test_set()
test_setattr()
test_slice()
test_sorted()
test_str()
test_sum()
test_super()
test_tuple()
test_type()
test_vars()
test_zip()
"""
