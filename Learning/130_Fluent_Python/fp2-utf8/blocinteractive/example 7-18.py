# Example 7-18. Demo of partial applied to the function tag from Example 7-9.

>>> from tagger import tag
>>> tag
<function tag at 0x10206d1e0>
>>> from functools import partial
>>> picture = partial(tag, 'img', class_='pic-frame')
>>> picture(src='wumpus.jpeg')
'<img class="pic-frame" src="wumpus.jpeg" />'
>>> picture
functools.partial(<function tag at 0x10206d1e0>, 'img', class_='pic-frame')
>>> picture.func
<function tag at 0x10206d1e0>
>>> picture.args
('img',)
>>> picture.keywords
{'class_': 'pic-frame'}
