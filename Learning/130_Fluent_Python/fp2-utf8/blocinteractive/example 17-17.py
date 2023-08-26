# Example 17-17. Mapping generator function examples

>>> list(enumerate('albatroz', 1))
[(1, 'a'), (2, 'l'), (3, 'b'), (4, 'a'), (5, 't'), (6, 'r'), (7, 'o'), (8, 'z')]
>>> import operator
>>> list(map(operator.mul, range(11), range(11)))
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
>>> list(map(operator.mul, range(11), [2, 4, 8]))
[0, 4, 16]
>>> list(map(lambda a, b: (a, b), range(11), [2, 4, 8]))
[(0, 2), (1, 4), (2, 8)]
>>> import itertools
>>> list(itertools.starmap(operator.mul, enumerate('albatroz', 1)))
['a', 'll', 'bbb', 'aaaa', 'ttttt', 'rrrrrr', 'ooooooo', 'zzzzzzzz']
>>> sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]
>>> list(itertools.starmap(lambda a, b: b / a, (itertools.accumulate(sample), 1)))
[5.0, 4.5, 3.66666666666665, 4.75, 5.2, 5.33333333333333, 5.0, 4.375, 4.88888888888889, 4.5]
