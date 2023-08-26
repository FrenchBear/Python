# Example 14-2. The __getitem__ of AnswerDict is bypassed by dict.update

>>> class AnswerDict(dict):
...     def __getitem__(self, key):
...         return 42
...
>>> ad = AnswerDict(a='foo')
>>> ad['a']
42
>>> d = {}
>>> d.update(ad)
>>> d['a']
'foo'
>>> d
{'a': 'foo'}
