# Example 31-18. Simplified pseudocode equivalent to the statement RESULT = yield from EXPR in the delegating generator (this covers the simplest case: .throw(…) and .close() are not supported; the only exception handled is StopIteration)

_i = iter(EXPR)
try:
    _y = next(_i)
except StopIteration as _e:
    _r = _e.value
else:
    while 1:
        _s = yield _y
        try:
            _y = _i.send(_s)
        except StopIteration as _e:
            _r = _e.value
            break

RESULT = _r
