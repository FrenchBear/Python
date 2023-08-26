# Example 17-20. count, cycle, pairwise, and repeat

>>> ct = itertools.count()
>>> next(ct)
0
>>> next(ct), next(ct), next(ct)
(1, 2, 3)
>>> list(itertools.islice(itertools.count(1, .3), 3))
[1, 1.3, 1.6]
>>> cy = itertools.cycle('ABC')
>>> next(cy)
'A'
>>> list(itertools.islice(cy, 7))
['B', 'C', 'A', 'B', 'C', 'A', 'B']
>>> list(itertools.pairwise(range(7)))
[(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]
>>> rp = itertools.repeat(7)
>>> next(rp), next(rp)
(7, 7)
>>> list(itertools.repeat(8, 4))
[8, 8, 8, 8]
>>> list(map(operator.mul, range(11), itertools.repeat(5)))
[0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
