# FrenchDeck_as_MutableSequence.py
# Make FrenchDeck a MutableSequence that supports random.shuffle
#
# 2023-08-06    PV

import collections
from collections.abc import MutableSequence
from random import shuffle

Card = collections.namedtuple('Card', ['rank', 'suit'])

class FrenchDeck(MutableSequence):
    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'spades diamonds clubs hearts'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]

    def __setitem__(self, position, card):
        self._cards[position] = card
    
    # Virtual methos must be implemented, otherwise can't register
    def __delitem__(self, item): pass
    def insert(self): pass
    # The rest is optional
    # def __iadd__(self): pass
    # def append(self): pass
    # def clear(self): pass
    # def extend(self): pass
    # def pop(self): pass
    # def reverse(self): pass
    # def remove(self): pass

print(issubclass(FrenchDeck, MutableSequence))

deck = FrenchDeck()
shuffle(deck)
print(deck[:5])
