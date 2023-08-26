# Example 29-1. A weak reference is a callable that returns the referenced object or None if the referent is no more

>>> import weakref
>>> a_set = {0, 1}
>>> wref = weakref.ref(a_set)
>>> wref
<weakref at 0x100637598; to 'set' at 0x100636748>
>>> wref()
{0, 1}
>>> a_set = {2, 3, 4}
>>> wref()
{0, 1}
>>> wref() is None
False
>>> wref() is None
True
