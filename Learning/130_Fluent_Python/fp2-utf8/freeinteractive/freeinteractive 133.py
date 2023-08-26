>>> import operator
>>> functools.reduce(operator.add, [sub[1] for sub in my_list], 0)
60
