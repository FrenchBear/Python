# Example 2-6. Cartesian product in a generator expression

>>> colors = ['black', 'white']
>>> sizes = ['S', 'M', 'L']
>>> for tshirt in (f'{c} {s}' for c in colors for s in sizes):
...     print(tshirt)
...
black S
black M
black L
white S
white M
white L
