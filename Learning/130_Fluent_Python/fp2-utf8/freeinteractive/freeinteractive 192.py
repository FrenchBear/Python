>>> from domainlib import multi_probe
>>> names = 'python.org rust-lang.org golang.org nolang.invalid'.split()
>>> gen_found = (name async for name, found in multi_probe(names) if found)
>>> gen_found
<async_generator object <genexpr> at 0x10a8f9700>
>>> async for name in gen_found:
...     print(name)
...
golang.org
python.org
rust-lang.org
