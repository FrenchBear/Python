# seq3.py
# Sequence of words, many ways of implementing an iterable object
# v3: Generator function
# 2021-05-18    PV

import re
import reprlib              # reprlib.repr shortens representations of very large objects
import collections.abc
from typing import Iterable, Iterator, Sequence

from isiterable import is_iterable

RE_WORD = re.compile(r'\w+')


class Sentence():
    def __init__(self, text: str) -> None:
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self) -> str:
        return f'Sentence({reprlib.repr(self.text)})'

    # A generator function returns a generator object, which is an Iterator
    def __iter__(self) -> Iterator:
        for word in self.words:
            yield word


if __name__ == '__main__':
    s = Sentence('"The time has come," the Walrus said')
    for word in s:
        print(word)
    print('Iterable from collections.abc: ', issubclass(Sentence, collections.abc.Iterable))   # True
    print('issubclass(Iterable):', issubclass(Sentence, Iterable))   # True, same thing
    print('isIterable:', is_iterable(s))
