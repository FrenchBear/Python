# seq1.py
# Sequence of words, many ways of implementing an iterable object
# v1: __getitem__ is enough to make Sentence1 enumerable.
# __len__ is for sequence protocol, but not needed to make Sentence1 iterable.
# 2021-05-17    PV

import re
import reprlib              # reprlib.repr shortens representations of very large objects
import collections.abc
from typing import Union

from collections.abc import Iterable

from isiterable import is_iterable

RE_WORD = re.compile(r'\w+')


class Sentence():
    def __init__(self, text: str) -> None:
        self.text = text
        self.words = RE_WORD.findall(text)

    def __getitem__(self, index: int | slice) -> str | list[str]:
        return self.words[index]

    def __len__(self) -> int:
        return len(self.words)

    def __repr__(self) -> str:
        return f'Sentence({reprlib.repr(self.text)})'


if __name__ == '__main__':
    s = Sentence('"The time has come," the Walrus said')
    # mypy complain, but it's wrong: seq1.py:43: error: "Sentence1" has no attribute "__iter__" (not iterable)
    for word in s:      # type: ignore[attr-defined]
        print(word)
    print('Iterable from collections.abc: ', issubclass(Sentence, collections.abc.Iterable))   # False
    # False because it does not implement __iter__
    print('issubclass(Iterable):', issubclass(Sentence, Iterable))   # False, same thing than above
    print('isIterable:', is_iterable(s))
