# gs.py
# game solver 12345+=
# 2022-02-23    PV

import itertools

cards = ['1','2','3','4','5','+','==']
#cards = ['1','2','3','4','4','6','+','==']

for l in itertools.permutations(cards):
    s = ''.join(l)
    #print(s)
    try:
        if eval(s):
            print(s)
    except:
        pass
