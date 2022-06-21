# Test of 3 doors game
# A simple 3 doors game, one car (V) is hidden behind one door, goats (C) are hidden behind the two other doors
# I choose a door (firstchoice), then game hosh opens a door with a goat behind.
# At this point, if I change my mind and select the other door (changemymind), then my changes to win increase.
# Winning with 1st choice is 33% probabiblity, changing my mind increase winning rate to 67%!
#
# 2022-06-21    PV

from random import shuffle, randint
from secrets import choice
from typing import Tuple


def game(verbose: bool) -> Tuple[str, str]:
    g = ['C', 'C', 'V']
    shuffle(g)

    firstchoice = randint(0, 2)
    anims = [(firstchoice+1) % 3, (firstchoice+2) % 3]
    shuffle(anims)
    anim = anims[0] if g[anims[0]] == 'C' else anims[1]
    changemymind = anims[1] if g[anims[0]] == 'C' else anims[0]
    if verbose:
        print(g, firstchoice, anims, anim, changemymind, g[firstchoice], g[changemymind])
        # print('Situation      ', g)
        # print('Initial choice ', choice1, '->', g[choice1])
        # print('Anim shows door', anim, '->', g[anim])
        # print('Change my mind ', newchoice, '->', g[newchoice])
        # print()
    assert(g[anim]) == 'C'

    return g[firstchoice], g[changemymind]


tests = 10000
verbose = False

winfirst = 0
winchangemymind = 0
for _ in range(tests):
    first, changemymind = game(verbose)
    if first == 'V':
        winfirst += 1
    if changemymind == 'V':
        winchangemymind += 1

print(tests, 'simulations:')
print('Win first choice:  ', winfirst, '=', format(winfirst/tests, '.1%'))
print('Win change my mind:', winchangemymind, '=', format(winchangemymind/tests, '.1%'))
