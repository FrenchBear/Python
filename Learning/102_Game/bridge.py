# bridge.py
# Combien de chemins pour aller de la case (0,0) à (4,2) sur un damier 3x5 passant par 4 cases noires et 3 cases blanches (0,0) étant noir?
# 2022-02-23    PV

sol = 0


def explore(r: int, c: int, prev: list[tuple[int, int]]):
    global sol
    prev2 = prev[:]
    prev2.append((r, c))
    if r == 4 and c == 2:
        b = sum(1 for (rs, cs) in prev2 if (rs+cs) % 2 == 0)
        w = sum(1 for (rs, cs) in prev2 if (rs+cs) % 2 == 1)
        if b == 4 and w == 3:
            print(prev2)
            sol += 1
        return
    if r < 4:
        explore(r+1, c, prev2)
    if c < 2:
        explore(r, c+1, prev2)


explore(0, 0, [])
print(sol)

