# gsp.py
# Grid Shorter Path
# From Programmation efficace p.51
#
# 2022-02-17    PV


# define weights of paths
w = {}
w['00->01'] = 3
w['00->11'] = 2
w['00->10'] = 1

w['01->02'] = 2
w['01->12'] = 1
w['01->11'] = 3

w['02->03'] = 1
w['02->13'] = 1
w['02->12'] = 1

w['03->13'] = 1

w['10->11'] = 4
w['10->21'] = 1
w['10->20'] = 0

w['11->12'] = 0
w['11->22'] = 1
w['11->21'] = 2

w['12->13'] = 1
w['12->23'] = 2
w['12->22'] = 0

w['13->23'] = 1

w['20->21'] = 2
w['21->22'] = 0
w['22->23'] = 1

rows = 3
cols = 4

# Visual check
for r in range(rows):
    for c in range(cols):
        print(f'[{r},{c}]', end='')
        if c != cols-1:
            ck = f'{r}{c}->{r}{c+1}'
            print(f'  {w[ck]}  ', end='')
        else:
            print()
    if r != rows-1:
        for c in range(cols):
            ck = f'{r}{c}->{r+1}{c}'
            print(f'  {w[ck]} ', end='')
            if c != cols-1:
                ck = f'{r}{c}->{r+1}{c+1}'
                print(f'   {w[ck]}  ', end='')
            else:
                print()


# calculate absolute distance to cells
ad = {}
for r in range(rows):
    for c in range(cols):
        ck = f'{r}{c}'                  # (current) cell key
        if r == 0:
            # First row cells, just one path from lect cell
            if c == 0:
                ad[ck] = (0, '__')      # Special predecessor to mark beginning of path
            else:
                lpk = f'{r}{c-1}'       # left predecessor key
                lak = f'{lpk}->{ck}'    # arc (from left predecessor) key
                ad[ck] = (ad[lpk][0] + w[lak], lpk)
        else:
            if c == 0:
                # First column cells, just one path from top cell
                tpk = f'{r-1}{c}'       # top predecessor key
                tak = f'{tpk}->{ck}'    # arc (from top predecessor) key
                ad[ck] = (ad[tpk][0] + w[tak], tpk)
            else:
                # Ordinary cell, three predecessors
                lpk = f'{r}{c-1}'       # left predecessor key
                lak = f'{lpk}->{ck}'    # arc (from left predecessor) key
                tpk = f'{r-1}{c}'       # top predecessor key
                tak = f'{tpk}->{ck}'    # arc (from top predecessor) key
                dpk = f'{r-1}{c-1}'     # diagonal predecessor key
                dak = f'{dpk}->{ck}'    # arc (from top predecessor) key

                l = [(ad[lpk][0] + w[lak], lpk), (ad[tpk][0] + w[tak], tpk), (ad[dpk][0] + w[dak], dpk)]
                ad[ck] = min(l)

# Shortest path
sp = []
r = rows-1
c = cols-1
ck = f'{r}{c}'                  # start from end cell and get back to cell 00 with predecessor __
l = ad[ck][0]
while ck != '__':
    sp.append(ad[ck])
    ck = ad[ck][1]
sp.reverse()
# print(sp)
for (_, ck) in sp[1:]:
    print(f'{ck} -> ', end='')
print(f'{r}{c},  l={l}')
