# tests_seq.py
# Tests of various implementations of Sentence class

from typing import Iterable, Iterator

import seq1
import seq2
import seq3
import seq4
import seq5
import seq6

from isiterable import is_iterable


def test_seq(Sentence, name: str):
    print('Testing', name)
    s = Sentence('Once upon a time...')
    print('  issubclass(Iterable):', issubclass(Sentence, Iterable))   # True, same thing
    print('  isIterable:', is_iterable(s))
    try:
        it: Iterator[str] = iter(s)
    except:
        print(name, 'is not iterable')
        print()
        return

    try:
        assert next(it) == 'Once'
        assert next(it) == 'upon'
        assert next(it) == 'a'
        assert next(it) == 'time'
    except:
        print(name, 'did not iterate over correct sequence')
        return

    try:
        _ = next(it)
        print(name, 'returned too many items')
        print()
        return
    except StopIteration:
        pass

    print('  Tests Ok!')
    print()


test_seq(seq1.Sentence, 'seq1')
test_seq(seq2.Sentence, 'seq2')
test_seq(seq3.Sentence, 'seq3')
test_seq(seq4.Sentence, 'seq4')
test_seq(seq5.Sentence, 'seq5')
test_seq(seq6.Sentence, 'seq6')
