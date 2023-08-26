import itertools

sample = [5, 4, 2, 8, 7, 6, 3, 0, 9, 1]

print(list(itertools.accumulate(sample)))
print(list(enumerate(itertools.accumulate(sample), 1)))
print(list(itertools.starmap(lambda a, b: b / a, enumerate(itertools.accumulate(sample), 1))))
