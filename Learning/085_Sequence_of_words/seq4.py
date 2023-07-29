# seq4.py
# Sequence of words, many ways of implementing an iterable object
# v4: Lazy implementation (generate words only when next is called)
# 2021-05-18    PV

import re
import reprlib              # reprlib.repr shortens representations of very large objects
import collections.abc
from typing import Iterable, Iterator

from isiterable import is_iterable

RE_WORD = re.compile(r'\w+')


class Sentence():
    def __init__(self, text: str) -> None:
        self.text = text

    def __repr__(self) -> str:
        return f'Sentence({reprlib.repr(self.text)})'

    # A generator function returns a generator object, which is an Iterator
    def __iter__(self) -> Iterator:
        for match in RE_WORD.finditer(self.text):   # note: it's not re.findall. finditer builds an iterator.
            yield match.group()


if __name__ == '__main__':
    s = Sentence('"The time has come," the Walrus said')
    for word in s:
        print(word)
    print('Iterable from collections.abc: ', issubclass(Sentence, collections.abc.Iterable))   # True
    print('issubclass(Iterable):', issubclass(Sentence, Iterable))   # True, same thing
    print('isIterable:', is_iterable(s))
