# sector_engine
# Sector game simulation, basic text interface
# 2020-08-17    PV

from random import randint
import re


class sector_engine:
    def __init__(self) -> None:
        self.sub_depth = randint(1, 3)
        self.sub_E = randint(25, 75)
        self.sub_N = randint(25, 75)
        while True:
            self.sub_dir_E = randint(-1, 1)
            self.sub_dir_N = randint(-1, 1)
            if self.sub_dir_E != 0 or self.sub_dir_N != 0:
                break

        self.b = 0
        self.boat_E = [25, 25, 30, 35]
        self.boat_N = [35, 30, 25, 25]
        self.boat_dir_E = [1, 1, 1, 1]
        self.boat_dir_N = [1, 1, 1, 1]
        self.boat_speed = [0, 0, 0, 0]
        self.moved = False
        self.fired = False

    def get_dist(self) -> int:
        d = max(abs(self.sub_N-self.boat_N[self.b]), abs(self.sub_E-self.boat_E[self.b]))
        return d

    def next_boat(self) -> None:
        self.b = (self.b + 1) % 4
        self.fired = False
        self.moved = False
        self.sub_E += self.sub_dir_E
        if self.sub_E < 25 or self.sub_E > 75:
            self.sub_dir_E = -self.sub_dir_E
            self.sub_E += 2*self.sub_dir_E
        self.sub_N += self.sub_dir_N
        if self.sub_N < 25 or self.sub_N > 75:
            self.sub_dir_N = -self.sub_dir_N
            self.sub_N += 2*self.sub_dir_N

    # Returns False if there is a problem (speed unchanged), True if speed has been set
    def set_speed(self, s: int) -> bool:
        if isinstance(s, int):
            if 0 <= s <= 9:
                self.boat_speed[self.b] = s
                return True
        return False

    def set_dir(self, dir_N: int, dir_E: int) -> bool:
        if isinstance(dir_N, int) and -1 <= dir_N <= 1 and isinstance(dir_E, int) and -1 <= dir_E <= 1 and abs(dir_E)+abs(dir_N) != 0:
            self.boat_dir_N[self.b] = dir_N
            self.boat_dir_E[self.b] = dir_E
            return True
        return False

    def move(self):
        if self.moved:
            return False     # Can only move once per turn
        new_N = self.boat_N[self.b] + self.boat_speed[self.b]*self.boat_dir_N[self.b]
        new_E = self.boat_E[self.b] + self.boat_speed[self.b]*self.boat_dir_E[self.b]
        if not (20 <= new_N <= 80 and 20 <= new_E <= 80):
            return False
        self.boat_N[self.b] = new_N
        self.boat_E[self.b] = new_E
        self.moved = True
        return True


# tests
se = sector_engine()


def direction(dir_N: int, dir_E: int) -> str:
    i = (dir_N+1)*3+(dir_E+1)
    return ['SW', 'S', 'SE', 'W', '0', 'E', 'NW', 'N', 'NE'][i]


def print_help():
    print("Sector Commands:")
    print("  q, quit:    Terminate game")
    print("  h, help:    Show help")
    print("  b, boats:   Show boats status")
    print("  n, next:    Select next boat, move submarine")
    print('  d, dist:    Show distance from current boat')
    print('  s#, speed#: Set current boat speed from 0 to 9')
    print('  dXX, dirXX: Set compass direction to XX, where XX in E, NE, N, NW, W, SW, S, SE')
    print('  m, move:    Move current boat')


print("Sector hunt starts!")
while True:
    print()
    print(f"sub: N={se.sub_N} E={se.sub_E} dir={direction(se.sub_dir_N, se.sub_dir_E)} depth={se.sub_depth}")
    print(
        f"boat {se.b+1}: N={se.boat_N[se.b]} E={se.boat_E[se.b]} dir={direction(se.boat_dir_N[se.b], se.boat_dir_E[se.b])} speed={se.boat_speed[se.b]}")
    if se.moved: print("Boat already moved")
    if se.fired: print("Boat already fired")

    print()
    rep = str.lower(str(input(f"[{se.b+1}] Command? ")))

    if rep == 'q' or rep == 'quit':
        break

    if rep == 'h' or rep == 'help':
        print_help()
        continue

    if rep == 'b' or rep == 'boats':
        for b in range(4):
            print(
                f"boat {b+1}: N={se.boat_N[b]} E={se.boat_E[b]} dir={direction(se.boat_dir_N[b], se.boat_dir_E[b])} speed={se.boat_speed[b]}")
        continue

    if rep == 'n' or rep == 'next':
        se.next_boat()
        continue

    if rep == 'd' or rep == 'dist':
        print(f"Distance: {se.get_dist()}")
        continue

    if ma := re.fullmatch(r"(s|speed) *([0-9])", rep):
        s = int(ma.group(2))
        if se.set_speed(s):
            print("Speed set successfully")
        else:
            print("Error setting speed")
        continue

    if ma := re.fullmatch(r"(d|dir) *(e|ne|n|nw|w|sw|s|se)", rep):
        d = str.lower(ma.group(2))
        ddir_N = {'e': 0, 'ne': 1, 'n': 1, 'nw': 1, 'w': 0, 'sw': -1, 's': -1, 'se': -1}
        ddir_E = {'e': 1, 'ne': 1, 'n': 0, 'nw': -1, 'w': -1, 'sw': -1, 's': 0, 'se': 1}
        dir_N = ddir_N.get(d, -2)
        dir_E = ddir_E.get(d, -2)
        if se.set_dir(dir_N, dir_E):
            print("Direction set successfully")
        else:
            print("Error setting direction")
        continue

    if rep == 'm' or rep == 'move':
        if se.move():
            print("Boat moved successfully")
        else:
            print("Error moving boat")
        continue

    print("Unknown command, enter h for help")
