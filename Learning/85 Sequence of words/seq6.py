# seq5.py
# Sequence of words, many ways of implementing an iterable object
# v6: yield from (but not a lazy implementation)
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

    def __repr__(self) -> str:
        return f'Sentence({reprlib.repr(self.text)})'

    # since findall is iterable, yields from it
    def __iter__(self) -> Iterator:
        yield from RE_WORD.findall(self.text)
        #return iter(RE_WORD.findall(self.text))        # Actually same thing


if __name__ == '__main__':
    s = Sentence('"The time has come," the Walrus said')
    for word in s:
        print(word)
    print('Iterable from collections.abc: ', issubclass(Sentence, collections.abc.Iterable))   # True
    print('issubclass(Iterable):', issubclass(Sentence, Iterable))   # True, same thing
    print('isIterable:', is_iterable(s))
