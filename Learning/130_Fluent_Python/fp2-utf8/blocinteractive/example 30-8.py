# Example 30-8. Binding the function signature from the tag function in Example 7-9 to a dict of arguments

>>> import inspect
>>> sig = inspect.signature(tag)
>>> my_tag = {'name': 'img', 'title': 'Sunset Boulevard',
...           'src': 'sunset.jpg', 'class_': 'framed'}
>>> bound_args = sig.bind(**my_tag)
>>> bound_args
<BoundArguments (name='img', class_='framed',
  attrs={'title': 'Sunset Boulevard', 'src': 'sunset.jpg'})>
>>> for name, value in bound_args.arguments.items():
...     print(name, '=', value)
...
name = img
class_ = framed
attrs = {'title': 'Sunset Boulevard', 'src': 'sunset.jpg'}
>>> del my_tag['name']
>>> bound_args = sig.bind(**my_tag)
Traceback (most recent call last):
  ...
TypeError: missing a required argument: 'name'
