try:
    c = complex(o)
except TypeError as exc:
    raise TypeError('o must be convertible to complex') from exc
