# Example 23-11. Behavior of a non-overriding descriptor

>>> obj = Managed()
>>> obj.non_over
-> Non-overriding.__get__(<Non-overriding object>, <Managed object>, <class Managed>)
>>> obj.non_over = 7
>>> obj.non_over
7
>>> Managed.non_over
-> Non-overriding.__get__(<Non-overriding object>, None, <class Managed>)
>>> del obj.non_over
>>> obj.non_over
-> Non-overriding.__get__(<Non-overriding object>, <Managed object>, <class Managed>)
