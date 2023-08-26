# Example 5-7. Frenchdeck.doctest: Adding a class attribute and a method to Card, the namedtuple from “A Pythonic Card Deck”

>>> Card.suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)
>>> def spades_high(card):
...     rank_value = FrenchDeck.ranks.index(card.rank)
...     suit_value = card.suit_values[card.suit]
...     return rank_value * len(card.suit_values) + suit_value
...
>>> Card.overall_rank = spades_high
>>> lowest_card = Card('2', 'clubs')
>>> highest_card = Card('A', 'spades')
>>> lowest_card.overall_rank()
0
>>> highest_card.overall_rank()
51
