# Example 17-18. Merging generator function examples

>>> list(itertools.chain('ABC', range(2)))
['A', 'B', 'C', 0, 1]
>>> list(itertools.chain(enumerate('ABC')))
[(0, 'A'), (1, 'B'), (2, 'C')]
>>> list(itertools.chain.from_iterable(enumerate('ABC')))
[0, 'A', 1, 'B', 2, 'C']
>>> list(zip('ABC', range(5), [10, 20, 30, 40]))
[('A', 0, 10), ('B', 1, 20), ('C', 2, 30)]
>>> list(itertools.zip_longest('ABC', range(5)))
[('A', 0), ('B', 1), ('C', 2), (None, 3), (None, 4)]
>>> list(itertools.zip_longest('ABC', range(5), fillvalue='?'))
[('A', 0), ('B', 1), ('C', 2), ('?', 3), ('?', 4)]
