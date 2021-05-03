# Deponia Chess Solver
# 2021-04   PV
#
# In a 4x6 grid, go from s (r=2, c=4) to e (r=0, c=1):
#   c 0   1   2   3   4   5
# r +---+---+---+---+---+---+
# 0 |   | e |   |   |   |   |
#   +---+---+---+---+---+---+
# 1 |   |   |   |   |   |   |
#   +---+---+---+---+---+---+
# 2 |   |   |   |   | s |   |
#   +---+---+---+---+---+---+
# 3 |   |   |   |   |   |   |
#   +---+---+---+---+---+---+
#
# Using only following movements (from o to A..F)
# +---+---+---+---+---+
# |   |   |   | A |   |
# +---+---+---+---+---+
# |   |   |   |   | B |
# +---+---+---+---+---+
# |   |   | o |   |   |
# +---+---+---+---+---+
# | F |   |   |   | C |
# +---+---+---+---+---+
# |   | E |   | D |   |
# +---+---+---+---+---+
#


hs = [1]*100    # Init with a initial pseudo 100 movement solution, since we only print solution better than previous one
ms = ''
def solve(h: list, m: str, r, c):
    # Hit end cell?
    if r == 0 and c == 1:
        global hs,ms
        # Only print solution if it's shorter than previous one
        if len(h) < len(hs):
            hs = h
            ms = m
            print(len(hs), hs)
            print(ms)
        return      # Continue exploring, in case we found later a better solution

    def trymove(dm, dr, dc):
        # Movement get out of grid, or we've already been there?  Don't continue
        if r+dr < 0 or r+dr > 3 or c+dc < 0 or c+dc > 5 or (r+dr, c+dc) in h:
            return
        h2 = list(h)                # Copy current list of moves
        h2.append((r+dr, c+dc))     # Add current move
        solve(h2, m+dm, r+dr, c+dc) # Continue using recursion, m+dm is the current string of movements with current move appended

    trymove('A', -2, 1)
    trymove('B', -1, 2)
    trymove('C', 1, 2)
    trymove('D', 2, 1)
    trymove('E', 2, -1)
    trymove('F', 1, -2)

r = 2
c = 4
solve([], '', r, c)
