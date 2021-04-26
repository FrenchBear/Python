
hs = [1]*100
ms = ''
def solve(h: list, m: str, r, c):
    if r == 0 and c == 1:
        global hs,ms
        if len(h) < len(hs):
            hs = h
            ms = m
            print(len(hs), hs)
            print(ms)
        return


    def trymove(dm, dr, dc):
        if r+dr < 0 or r+dr > 3 or c+dc < 0 or c+dc > 5 or (r+dr, c+dc) in h:
            return
        h2 = list(h)
        h2.append((r+dr, c+dc))
        solve(h2, m+dm, r+dr, c+dc)

    trymove('A', -2, 1)
    trymove('B', -1, 2)
    trymove('C', 1, 2)
    trymove('D', 2, 1)
    trymove('E', 2, -1)
    trymove('F', 1, -2)


r = 2
c = 4
solve([], '', r, c)
