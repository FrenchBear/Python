# Pythin built-in functions
# Learning Python
# From https://docs.python.org/3/library/functions.html
# 2016-08-10    PV

import sys
from os import system

system('chcp 65001 >nul')
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)


def test_abs():
    print('\ntest_abs()')
    i = -2
    f = -3.25
    c = complex(3, 4)
    print('\tabs({0}) = {1}'.format(i, abs(i)))
    print('\tabs({0}) = {1}'.format(f, abs(f)))
    print('\tabs({0}) = {1}'.format(c, abs(c)))


def test_all():
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
    Convert an integer number to a binary string. The result is a valid Python expression. If x is not a Python int object, it has to define an __index__() method that returns an integer.
    """
    print('\ntest_bin()')
    print('\tbin({0:x}) = {1}'.format(0xCAFE, bin(0xCAFE)))
    print('\tbin({0:x}) = {1}'.format(0xDEADBEEF, bin(0xDEADBEEF)))


def test_bool():
    """
    bool([x])
    Convert a value to a Boolean, using the standard truth testing procedure. If x is false or omitted, this returns False; otherwise it returns True. bool is also a class, which is a subclass of int. Class bool cannot be subclassed further. Its only instances are False and True.
    """
    print('\ntest_bool()')
    print('\tbool({0}) = {1}'.format(0, bool(0)))
    print('\tbool({0}) = {1}'.format(23, bool(23)))


def test_bytearray():
    """
    bytearray([source[, encoding[, errors]]])

    Return a new array of bytes. The bytearray type is a mutable sequence of integers in the range 0 <= x < 256. It has most of the usual methods of mutable sequences, described in Mutable Sequence Types, as well as most methods that the bytes type has, see Bytes and Byte Array Methods.

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

    # Unicode é U+00E9, UTF-8: 0xC3 0xA9, UTF-16: 0x00E9, UTF-32: 0x000000E9.  Decomposition: U+0301-U+0065.  Uppercase: É U+00C9
    # Unicode Beamed eighth notes ♫ U+266B, UTF-8: 0xE2 0x99 0xAB, UTF-16: 0x266B, UTF-32: 0x0000266B
    # Unicode Musical symbol G clef 𝄞 U+1D11E, UTF-8: 0xF0 0x9D 0x84 0x9E, UTF-16: 0xD834 0xDD1E, UTF-32: 0x0001D11E
    # Copyleft 🄯
    # Unicode Boar 🐗 U+1F417, UTF-8: 0xF0 0x9F 0x90 0x97, UTF-16: 0xD83D 0xDC17, UTF-32: 0x0001F417
    
    ba16 = bytearray("Café♫🐗", "utf-16")
    print('\tutf-16 -> ', list(ba16))
    m16 = memoryview(ba16).cast('H')
    print('\tm16 ->    ', [hex(c) for c in m16.tolist()])

    ba32 = bytearray("Café♫🐗", "utf-32")
    print('\tutf-32 -> ', list(ba32))
    m32 = memoryview(ba32).cast('L')
    print('\tm32 ->    ', [hex(c) for c in m32.tolist()])

 
def test_bytes():
    print('\ntest_bytes()')


def test_callable():
    print('\ntest_callable()')


def test_chr():
    print('\ntest_chr()')


def test_classmethod():
    print('\ntest_classmethod()')


def test_compile():
    print('\ntest_compile()')


def test_complex():
    print('\ntest_complex()')


def test_delattr():
    print('\ntest_delattr()')


def test_dict():
    print('\ntest_dict()')


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


def test_staticmethod():
    print('\ntest_staticmethod()')


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
test_bytearray()
"""
test_bytes()
test_callable()
test_chr()
test_classmethod()
test_compile()
test_complex()
test_delattr()
test_dict()
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
test_staticmethod()
test_str()
test_sum()
test_super()
test_tuple()
test_type()
test_vars()
test_zip()
"""
