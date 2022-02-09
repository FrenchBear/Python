=================
Tombola Tests
=================

Every concrete subclass of Tombola should pass the tests.

Create and load instance from iterable::

    >>> balls = list(range(3))
    >>> globe = ConcreteTombola(balls)
    >>> globe.loaded()
    True
    >>> globe.inspect()
    (0, 1, 2)
    