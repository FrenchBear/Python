# Layton Unwound Future Puzzle 70
# 2022-03-08    PV

# T represents a 5x5 matrix, each cell contains a tuple (plugs, paths...)
# plugs is a string 'nesw' where N is the number of links North (0..2), E the number of East links...
# paths is a series of tuples 'inout' where in and out are a letter and a number, letter in nesw, number 0 if there is
# just 1 connector on this side, otherwise 1 or 2 to indicate first and second connectors on the sie (clock orientation)

import itertools

T: list[list[tuple[str, ...]]]
T = [
    [('0110', 'e0s0'), ('0101', 'e0w0'), ('0121', 'e0w0', 's1s2'), ('0101', 'e0w0'), ('2011', 'n1s0', 'n2w0')],
    [('1210', 'n0e2', 'e1s0'), ('0222', 'e1w1', 'e2s2', 's1w2'), ('2112', 'n1s0', 'n2w1', 'e0w2'),
            ('0121', 'e0s2', 's1w0'), ('1021', 'n0s2', 's1w0')],
    [('1210', 'n0e2', 'e1s0'), ('2112', 'n1w1', 'n2e0', 's0w2'), ('1221', 'n0w0', 'e1s2', 'e2s1'), 
            ('2112', 'n1s0', 'n2w2', 'e0w1'), ('2011', 'n1n2', 's0w0')],
    [('1210', 'n0e2', 'e1s0'), ('1212', 'n0e1', 'e2w2', 's0w1'),
     ('2002', 'n1w1', 'n2w2'), ('1210', 'n0e1', 'e2s0'), ('1012', 'n0s0', 'w1w2')],
    [('1120', 'n0s1', 'e0s2'), ('1201', 'n0e2', 'e1w0'), ('0202', 'e1w1', 'e2w2'),
     ('1102', 'n0w1', 'e0w2'), ('1021', 'n0s1', 's2w0')]
]

# Verification
for i in range(5):
    for j in range(5):
        cell = T[i][j]
        plugs = cell[0]
        plugsdic = {'n': int(plugs[0]), 'e': int(plugs[1]), 's': int(plugs[2]), 'w': int(plugs[3])}
        paths = cell[1:]
        verif = {'n': 0, 'e': 0, 's': 0, 'w': 0}
        for path in paths:
            p1 = path[0]
            n1 = int(path[1])
            p2 = path[2]
            n2 = int(path[3])
            verif[p1] += 1
            verif[p2] += 1
            if n1 == 0:
                assert(plugsdic[p1] == 1)
            elif n1 == 1 or n1 == 2:
                assert(plugsdic[p1] == 2)
            else:
                breakpoint()
            if n2 == 0:
                assert(plugsdic[p2] == 1)
            elif n2 == 1 or n2 == 2:
                assert(plugsdic[p2] == 2)
            else:
                breakpoint()

        assert plugsdic == verif


def check_connexions(t: list[list[tuple[str, ...]]]) -> str:
    startcell = t[0][4]
    startplugs = startcell[0]
    if startplugs[0] != '2':
        return 'Invalid start cell'

    def find_connex(paths: tuple[str, ...], input: str) -> str:
        for path in paths:
            if path[0:2] == input:
                return path[2:]
            if path[2:] == input:
                return path[0:2]
        return ''

    def perm(s: str) -> str:
        if s == '0':
            return '0'
        elif s == '1':
            return '2'
        else:
            return '1'

    def checkpath(n: int) -> str:
        r = 0
        c = 4
        input = 'n'+str(n)
        while 0 <= r < 5 and 0 <= c < 5:
            cell = t[r][c]
            paths = cell[1:]
            output = find_connex(paths, input)
            if output == '':
                return 'no connex'
            if output[0] == 'n':
                input = 's'+perm(output[1])
                r -= 1
            elif output[0] == 'e':
                input = 'w'+perm(output[1])
                c += 1
            elif output[0] == 's':
                input = 'n'+perm(output[1])
                r += 1
            elif output[0] == 'w':
                input = 'e'+perm(output[1])
                c -= 1
            if r == 5 and c == 0:
                return '(5,0)'
            if r == 5 and c == 4:
                return '(5,4)'
        return 'Out of area'

    e1 = checkpath(1)
    e2 = checkpath(2)
    return '1:'+e1+', 2:'+e2


#print(check_connexions(T))


def exchange_cells(cc1: tuple[int, int], cc2: tuple[int, int]) -> list[list[tuple[str, ...]]]:
    newt: list[list[tuple[str, ...]]] = []
    for r in range(5):
        newt.append(T[r].copy())
    r1 = cc1[0]
    c1 = cc1[1]
    r2 = cc2[0]
    c2 = cc2[1]
    newt[r1][c1], newt[r2][c2] = newt[r2][c2], newt[r1][c1]
    return newt


# Build a dict of potentially interchangeable cells (same plugs)
celltypedic: dict[str, list[tuple[int, int]]] = {}
for i in range(5):
    for j in range(5):
        cell = T[i][j]
        plugs = cell[0]
        if plugs in celltypedic:
            celltypedic[plugs].append((i, j))
        else:
            celltypedic[plugs] = [(i, j)]

for k, v in celltypedic.items():
    if len(v) > 1:      # Interchangeable if there are at least 2 cells with same plugs
        print(k, v)
        # Explore all combinations of 2 cells
        for couple in itertools.combinations(v, 2):
            print('  ', couple)
            c1 = couple[0]
            c2 = couple[1]
            newt = exchange_cells(c1, c2)
            sol = check_connexions(newt)
            print('    ', sol)
            if sol=='1:(5,4), 2:(5,4)':
                print('*********** Solution found')
