# Example 22-24. Instance attribute does not shadow the class property continued from Example 22-23

>>> Class.prop
<property object at 0x1072b7408>
>>> obj.prop
'the prop value'
>>> obj.prop = 'foo'
Traceback (most recent call last):
  ...
AttributeError: can't set attribute
>>> obj.__dict__['prop'] = 'foo'
>>> vars(obj)
{'data': 'bar', 'prop': 'foo'}
>>> obj.prop
'the prop value'
>>> Class.prop = 'baz'
>>> obj.prop
'foo'
