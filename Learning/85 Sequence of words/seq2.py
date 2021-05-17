# seq2.py
# Sequence of words, many ways of implementing an iterable object
# v2: Classic iterator, using a separate class
# 2021-05-17    PV

import re
import reprlib              # reprlib.repr shortens representations of very large objects
import collections.abc
from typing import Iterable, Iterator, Sequence

RE_WORD = re.compile(r'\w+')

class Sentence1():
    def __init__(self, text:str) -> None:
        self.text=text
        self.words=RE_WORD.findall(text)

    def __repr__(self) -> str:
        return f'Sentence({reprlib.repr(self.text)})'

    def __iter__(self) -> Iterator:
        return SentenceIterator(self.words)


class SentenceIterator:
    def __init__(self, words:Sequence[str]) -> None:
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


# Goot method to chef if s is iterable: iter(s) should not return an error.
# iter() works if s has only __getitem__, while for abc.Iterable it needs __iter__.
def isIterable(s) -> bool:
    try:
        _ = iter(s)
    except TypeError:
        return False
    except Exception as ex:
        raise ex
    return True


if __name__=='__main__':
    s = Sentence1('"The time has come," the Walrus said')
    for word in s:
        print(word)
    print('Iterable from collections.abc: ', issubclass(Sentence1, collections.abc.Iterable))   # True
    # False because it does not implement __iter__
    print('isIterable:', isIterable(s))
