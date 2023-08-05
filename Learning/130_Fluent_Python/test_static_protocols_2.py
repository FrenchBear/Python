# test_static_protocols_2.py
# fluent python chapter 12
#
# 2023-08-05    PV

from abc import abstractmethod
import collections
from collections import abc
from typing import Protocol, runtime_checkable

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck:
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                                        for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position) -> Card:
        return self._cards[position]
abc.Sequence.register(FrenchDeck)       # type: ignore      # Pylance should not complain about this

print('Iterable', issubclass(FrenchDeck, abc.Iterable))
print('Container', issubclass(FrenchDeck, abc.Container))
print('Sized', issubclass(FrenchDeck, abc.Sized))
print('Collection', issubclass(FrenchDeck, abc.Collection))
print('Sequence', issubclass(FrenchDeck, abc.Sequence))
print()

@runtime_checkable
class SupportsSequence(Protocol):
    @abstractmethod
    def __getitem__(self, index): pass
    @abstractmethod
    def __len__(self): pass

print('SupportsSequence', issubclass(FrenchDeck, SupportsSequence))
print()

deck = FrenchDeck()
c1 = Card('7', 'diamonds')
print(c1 in deck) # type: ignore  # __contains__ automatically provided, despite mypy complaining about it
print(reversed(deck))             # __reversed__ automatically provided
