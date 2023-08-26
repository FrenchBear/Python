# Example 22-25. New class property shadows the existing instance attribute (continued from Example 22-24)

>>> obj.data
'bar'
>>> Class.data
'the class data attr'
>>> Class.data = property(lambda self: 'the "data" prop value')
>>> obj.data
'the "data" prop value'
>>> del Class.data
>>> obj.data
'bar'
