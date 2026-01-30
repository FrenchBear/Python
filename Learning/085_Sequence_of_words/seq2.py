# seq2.py
# Sequence of words, many ways of implementing an iterable object
# v2: Classic iterator, using a separate class
# 2021-05-17    PV

import re
import reprlib              # reprlib.repr shortens representations of very large objects
from collections.abc import Sequence, Iterable
from collections.abc import Iterator

from isiterable import is_iterable

RE_WORD = re.compile(r'\w+')


class Sentence():
    def __init__(self, text: str) -> None:
        self.text = text
        self.words = RE_WORD.findall(text)

    def __repr__(self) -> str:
        return f'Sentence({reprlib.repr(self.text)})'

    def __iter__(self) -> Iterator:
        return SentenceIterator(self.words)


# Classic basic iterator, with no generator expression or yield keyword, a call to __next__
# just returns next item or StopIteration
class SentenceIterator:
    def __init__(self, words: Sequence[str]) -> None:
        self.words = words
        self.index = 0

    def __next__(self) -> str:
        try:
            word = self.words[self.index]
            self.index += 1
        except IndexError:
            raise StopIteration()
        return word

    def __iter__(self) -> Iterator:
        return self


if __name__ == '__main__':
    s = Sentence('"The time has come," the Walrus said')
    for word in s:
        print(word)
    print('Iterable from collections.abc: ', issubclass(Sentence, Iterable))   # True
    print('issubclass(Iterable):', issubclass(Sentence, Iterable))   # True, same thing
    print('isIterable:', is_iterable(s))
