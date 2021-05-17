# seq1.py
# Sequence of words, many ways of implementing an iterable object
# v1: __getitem__ is enough to make Sentence1 enumerable.  
# __len__ is for sequence protocol, but not needed to make Sentence1 iterable.
# 2021-05-17    PV

import re
import reprlib              # reprlib.repr shortens representations of very large objects
import collections.abc
from typing import Union

RE_WORD = re.compile(r'\w+')

class Sentence1():
    def __init__(self, text:str) -> None:
        self.text=text
        self.words=RE_WORD.findall(text)

    def __getitem__(self, index: Union[int, slice]) -> Union[str, list[str]]:
        return self.words[index]

    def __len__(self) -> int:
        return len(self.words)

    def __repr__(self) -> str:
        return f'Sentence({reprlib.repr(self.text)})'


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
    # mypy complain, but it's wrong: seq1.py:43: error: "Sentence1" has no attribute "__iter__" (not iterable)
    for word in s:
        print(word)
    print('Iterable from collections.abc: ', issubclass(Sentence1, collections.abc.Iterable))   # False
    # False because it does not implement __iter__
    print('isIterable:', isIterable(s))
