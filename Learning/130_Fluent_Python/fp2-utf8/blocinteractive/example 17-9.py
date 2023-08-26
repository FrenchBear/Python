# Example 17-9. The gen_AB generator function is used by a list comprehension, then by a generator expression

>>> def gen_AB():
...     print('start')
...     yield 'A'
...     print('continue')
...     yield 'B'
...     print('end.')
...
>>> res1 = [x*3 for x in gen_AB()]
start
continue
end.
>>> for i in res1:
...     print('-->', i)
...
--> AAA
--> BBB
>>> res2 = (x*3 for x in gen_AB())
>>> res2
<generator object <genexpr> at 0x10063c240>
>>> for i in res2:
...     print('-->', i)
...
start
--> AAA
continue
--> BBB
end.
