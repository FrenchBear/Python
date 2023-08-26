# Example 15-5. Using a BookDict, but not quite as intended

>>> from books import BookDict
>>> pp = BookDict(title='Programming Pearls',
...               authors='Jon Bentley',
...               isbn='0201657880',
...               pagecount=256)
>>> pp
{'title': 'Programming Pearls', 'authors': 'Jon Bentley', 'isbn': '0201657880', 'pagecount': 256}
>>> type(pp)
<class 'dict'>
>>> pp.title
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'dict' object has no attribute 'title'
>>> pp['title']
'Programming Pearls'
>>> BookDict.__annotations__
{'isbn': <class 'str'>, 'title': <class 'str'>, 'authors': typing.List[str],  'pagecount': <class 'int'>}
