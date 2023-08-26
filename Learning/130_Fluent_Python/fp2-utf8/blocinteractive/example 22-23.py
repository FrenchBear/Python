# Example 22-23. Instance attribute shadows the class data attribute

>>> class Class:
...     data = 'the class data attr'
...     @property
...     def prop(self):
...         return 'the prop value'
...
>>> obj = Class()
>>> vars(obj)
{}
>>> obj.data
'the class data attr'
>>> obj.data = 'bar'
>>> vars(obj)
{'data': 'bar'}
>>> obj.data
'bar'
>>> Class.data
'the class data attr'
