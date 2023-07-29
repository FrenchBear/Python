from collections.abc import Sequence, Iterable
from typing import Any, Iterator, overload

s1 = set(dir(Iterable))     # Base: iter()  = IEnumerable
s2 = set(dir(Sequence))     # Add reversed(), len(), in, count, getitem/[]

# print(s1)
# print(s2-s1)

# print(Iterable.__abstractmethods__)


class It1(Iterable):
    def __init__(self, e: Iterable) -> None:
        super().__init__()
        self.li = list(e)

    def __iter__(self) -> Iterator:
        return iter(self.li)


i1 = It1([1, 2, 3])
for i in i1:
    print(i)

# print(Sequence.__abstractmethods__)


class It2(It1, Sequence):
    def __init__(self, e: Iterable) -> None:
        super().__init__(e)

    def __len__(self):
        return len(self.li)

    def __getitem__(self, index: slice | int) -> Any:
        return self.li[index]


i2 = It2('abcde')
print(len(i2))
print(''.join(reversed(i2)))
print(i2[::-1])
