# Example 16-19. bingoaddable.py: AddableBingoCage extends BingoCage to support + and +=

from tombola import Tombola
from bingo import BingoCage

class AddableBingoCage(BingoCage):
    def __add__(self, other):
        if isinstance(other, Tombola):
            return AddableBingoCage(self.inspect() + other.inspect())
        else:
            return NotImplemented

    def __iadd__(self, other):
        if isinstance(other, Tombola):
            other_iterable = other.inspect()
        else:
            try:
                other_iterable = iter(other)
            except TypeError:
                msg = ("right operand in += must be 'Tombola' or an iterable")
                raise TypeError(msg)
        self.load(other_iterable)
        return self
