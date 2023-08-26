# Example 24-1. Testing record_factory, a simple class factory

>>> Dog = record_factory('Dog', 'name weight owner')
>>> rex = Dog('Rex', 30, 'Bob')
>>> rex
Dog(name='Rex', weight=30, owner='Bob')
>>> name, weight, _ = rex
>>> name, weight
('Rex', 30)
>>> "{2}'s dog weighs {1}kg".format(*rex)
"Bob's dog weighs 30kg"
>>> rex.weight = 32
>>> rex
Dog(name='Rex', weight=32, owner='Bob')
>>> Dog.__mro__
(<class 'factories.Dog'>, <class 'object'>)
