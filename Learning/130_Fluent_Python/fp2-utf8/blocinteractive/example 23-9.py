# Example 23-9. Behavior of an overriding descriptor

>>> obj = Managed()
>>> obj.over()
-> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
>>> Managed.over
-> Overriding.__get__(<Overriding object>, None, <class Managed>)
>>> obj.over = 7
-> Overriding.__set__(<Overriding object>, <Managed object>, 7)
>>> obj.over
-> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
>>> obj.__dict__['over'] = 8
>>> vars(obj)
{'over': 8}
>>> obj.over
-> Overriding.__get__(<Overriding object>, <Managed object>, <class Managed>)
