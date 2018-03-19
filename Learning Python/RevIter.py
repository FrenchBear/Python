# Reverse iterator

import random

class RevIter:
    def __init__(self, data):
        self.data = data
        self.index = len(data)

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == 0:
            raise StopIteration
        self.index -= 1
        return self.data[self.index]

revi = RevIter([2,3,5,7,11,13])
for i in revi:
    print(i)
print()


class RandomIter:
    def __init__(self, data):
        self.data = data

    def __iter__(self):
        self.index = len(self.data)
        self.indexes = list(range(len(self.data)))
        random.shuffle(self.indexes)
        return self

    def __next__(self):
        if self.index==0:
            raise StopIteration
        self.index -= 1
        return self.data[self.indexes[self.index]]

rndi = RandomIter([2,3,5,7,11,13])
for i in rndi:
    print(i)

