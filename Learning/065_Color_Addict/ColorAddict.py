# ColorAddict.py
# Simulation of card game
# 2020-01-05    PV

# Règle: on a 3 cartes retournées, si on ne peut pas jouer parmi les cartes retournées
# on en retourne une de plus et on passe son tour, si on peut jouer, on en retourne une de plus s'il
# y en a moins de trois retournées.
# Si les deux joueurs sont bloqués, cette version arrête la simulation et retourne "Game stuck"

from enum import Enum, auto
from collections import namedtuple, Counter
from typing import Optional
from random import shuffle
from pprint import pprint


class Color(Enum):
    JOKER = 0
    VERT = auto()
    MAUVE = auto()
    BRUN = auto()
    NOIR = auto()
    ROUGE = auto()
    JAUNE = auto()
    GRIS = auto()
    ORANGE = auto()
    ROSE = auto()
    BLEU = auto()


# Trick to override __repr__ or __str__ of a named tuple
# noqua: #Linter should not check this line


class Card(namedtuple("Card", ["Text", "Ink"])):  # noqa
    __slots__ = ()

    def __repr__(self):
        return "Card(t=" + self.Text.name + ",i=" + self.Ink.name + ")"


def PlayGame() -> tuple[list[Card], list[Card], list[Card]]:
    Cards: list[Card] = [Card(t, i) for t in Color if t != Color.JOKER for i in Color]
    shuffle(Cards)
    Decks = [Cards[:55], Cards[55:]]
    Visible = [3, 3]
    top: Card | None = None
    Played: list[Card] = []

    def Play(player: int) -> tuple[Card | None, bool]:
        if top is None:
            # Visible[player] remains 3
            return (Decks[player].pop(0), False)

        for i in range(Visible[player]):
            c = Decks[player][i]
            if (
                c.Text == top.Text
                or c.Text == top.Ink
                or c.Ink == top.Text
                or c.Ink == top.Ink
            ):
                del Decks[player][i]
                Visible[player] -= 1
                # Keep at list 3 visible cards
                if Visible[player] < 3 and Visible[player] < len(Decks[player]):
                    Visible[player] += 1
                return c, False

        if Visible[player] < len(Decks[player]):
            Visible[player] += 1
            return (None, False)
        else:
            return (None, True)

    while True:
        (c1, stuck1) = Play(0)
        if c1:
            top = c1
            Played.append(c1)

        (c2, stuck2) = Play(1)
        if c2:
            top = c2
            Played.append(c2)

        if stuck1 and stuck2:
            break

    return (Played, Decks[0], Decks[1])


def PlayOneGame():
    (Played, Deck0, Deck1) = PlayGame()
    if len(Deck0) == 0:
        if len(Deck1) == 0:
            print("Both Player 1 and Player 2 won")
        else:
            print(f"Player 1 won, Player 2 has {len(Deck1)} card(s)")
    elif len(Deck1) == 0:
        print(f"Player 2 won, Player 1 has {len(Deck0)} card(s)")
    else:
        print(
            f"Game stuck, Player 1 has {len(Deck0)} card(s), Player 2 has {len(Deck1)} card(s)"
        )

    print(Played)
    print("Player 1:", end="")
    pprint(Deck0)
    print("\nPlayer 2:", end="")
    pprint(Deck1)


# PlayOneGame()


def ComputeStats() -> None:
    c:Counter[int] = Counter()
    for i in range(1000):
        (_, Deck0, Deck1) = PlayGame()

        winner: int
        if len(Deck0) == 0:
            if len(Deck1) == 0:
                winner = 3
            else:
                winner = 1
        elif len(Deck1) == 0:
            winner = 2
        else:
            winner = 0
        c[winner] += 1
    print(
        "On 1000 games: 0: Game stuck, 1: Player 1 wins, 2: Player 2 wins, 3: Both players win"
    )
    print(c.most_common())


ComputeStats()
