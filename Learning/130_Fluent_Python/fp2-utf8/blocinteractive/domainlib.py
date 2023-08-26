# Example 21-16. Experimenting with domainlib.py after running python3 -m asyncio

>>> await asyncio.sleep(3, 'Rise and shine!')
'Rise and shine!'
>>> from domainlib import *
>>> await probe('python.org')
Result(domain='python.org', found=True)
>>> names = 'python.org rust-lang.org golang.org nolang.invalid'.split()
>>> async for result in multi_probe(names):
...     print(*result, sep='\t')
...
golang.org      True
no-lang.invalid False
python.org      True
rust-lang.org   True
