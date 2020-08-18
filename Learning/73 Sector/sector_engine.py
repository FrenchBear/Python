# sector_engine
# Sector game simulation, basic text interface
# 2020-08-17    PV

from random import randint
import re
from typing import Tuple


class sector_engine:
    def __init__(self) -> None:
        self.sub_depth = randint(1, 3)
        self.sub_E = randint(30, 70)
        self.sub_N = randint(30, 70)
        while True:
            self.sub_dir_E = randint(-1, 1)
            self.sub_dir_N = randint(-1, 1)
            if self.sub_dir_E != 0 or self.sub_dir_N != 0:
                break

        self.b = 0
        self.boat_N = [35, 30, 25, 25]
        self.boat_E = [25, 25, 30, 35]
        self.boat_dir_N = [1, 1, 1, 1]
        self.boat_dir_E = [1, 1, 1, 1]
        self.boat_speed = [0, 0, 0, 0]
        self.moved = False
        self.fired = False
        self.fire_N = 0
        self.fire_E = 1

    # Returns distance of current boat to sub, and a boolean True if in firing range
    def get_dist(self) -> Tuple[int, bool]:
        dN = abs(self.sub_N-self.boat_N[self.b])
        dE = abs(self.sub_E-self.boat_E[self.b])
        d = max(dN, dE)
        canfire = False
        if d <= 1:
            canfire = True
        if d == 2:
            canfire = dN != 1 and dE != 1
        return (d, canfire)

    def next_boat(self) -> None:
        self.b = (self.b + 1) % 4
        self.moved = False
        self.fired = False
        self.sub_E += self.sub_dir_E
        # Sub only navigates between coord 30 and 70 on both directions
        if self.sub_E < 30 or self.sub_E > 70:
            self.sub_dir_E = -self.sub_dir_E
            self.sub_E += 2*self.sub_dir_E
        self.sub_N += self.sub_dir_N
        if self.sub_N < 30 or self.sub_N > 70:
            self.sub_dir_N = -self.sub_dir_N
            self.sub_N += 2*self.sub_dir_N

    # Returns False if there is a problem (speed unchanged), True if speed has been set
    def set_speed(self, s: int) -> bool:
        if isinstance(s, int):
            if 0 <= s <= 9:
                self.boat_speed[self.b] = s
                return True
        return False

    # Returns False if there is a problem (direction unchanged), True if direction has been set
    def set_dir(self, dir_N: int, dir_E: int) -> bool:
        if isinstance(dir_N, int) and -1 <= dir_N <= 1 and isinstance(dir_E, int) and -1 <= dir_E <= 1 and abs(dir_E)+abs(dir_N) != 0:
            self.boat_dir_N[self.b] = dir_N
            self.boat_dir_E[self.b] = dir_E
            return True
        return False

    def move(self) -> Tuple[str, bool]:
        if self.moved:
            return ('Already moved', False)     # Can only move once per turn
        new_N = self.boat_N[self.b] + self.boat_speed[self.b]*self.boat_dir_N[self.b]
        new_E = self.boat_E[self.b] + self.boat_speed[self.b]*self.boat_dir_E[self.b]
        if not (20 <= new_N <= 80 and 20 <= new_E <= 80):
            return ("Can't move outside of 25-75 grid", False)

        self.moved = True

        if self.occupied(new_N, new_E):
            self.bump()
            return ('Collision!  Bumped!', False)

        self.boat_N[self.b] = new_N
        self.boat_E[self.b] = new_E
        return ('', True)

    # Returns False if there is a problem (fire direction unchanged), True if fire direction has been set
    def set_fire_dir(self, fire_N: int, fire_E: int) -> bool:
        if isinstance(fire_N, int) and -1 <= fire_N <= 1 and isinstance(fire_E, int) and -1 <= fire_E <= 1 and abs(fire_E)+abs(fire_N) != 0:
            self.fire_N = fire_N
            self.fire_E = fire_E
            return True
        return False

    # Returns a string status, and False if there is a problem or True if Ok
    def fire(self, depth: int) -> Tuple[str, bool]:
        if self.fired:
            return ('Already fired', False)
        if isinstance(depth, int):
            self.fired = True

            if 1 <= depth <= 3:
                # Check that we're in firing range
                (dist, canfire) = self.get_dist()
                if not canfire:
                    self.bump()
                    return ('Not in firing range, bumped!', False)

                # Check that direction is correct
                if self.boat_N[self.b] + self.fire_N*dist != self.sub_N or self.boat_E[self.b] + self.fire_E*dist != self.sub_E:
                    self.bump()
                    return('Fired in wrong direction, bumped!', False)

                # Check depth
                if self.sub_depth == depth:
                    return('Sumbarine hit! You won!', True)
                return(f'Almost hit submarine! Depth offset={abs(self.sub_depth-depth)}', True)

                self.canfire = False    # Can only fire once per turn
                return ('ToDo', True)
        return ('Arg err', False)

    def bump(self):
        while True:
            # Chose random direction
            while True:
                self.boat_dir_N[self.b] = randint(-1, 1)
                self.boat_dir_E[self.b] = randint(-1, 1)
                if self.boat_dir_N[self.b] != 0 or self.boat_dir_E[self.b] != 0:
                    break
            new_N = self.boat_N[self.b] + self.boat_dir_N[self.b]*self.boat_speed[self.b]
            new_E = self.boat_E[self.b] + self.boat_dir_E[self.b]*self.boat_speed[self.b]
            if not self.occupied(new_N, new_E) and 25 <= new_N <= 75 and 25 <= new_E <= 75:
                break

    # Check if cell (N, E) is occupied by a different boat than current boat
    def occupied(self, N: int, E: int) -> bool:
        for lb in range(4):
            if lb != self.b:
                if N == self.boat_N[lb] and E == self.boat_E[lb]:
                    return True
        return False

    # For tests
    def jump(self, N: int, E: int) -> bool:
        if isinstance(N, int) and isinstance(E, int):
            if 20 <= N <= 80 and 20 <= E <= 80:
                self.boat_N[self.b] = N
                self.boat_E[self.b] = E
                # No collision detection here, maybe we should...
                return True
        return False


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
    print('  fXX, fireXX: Set fire direction to XX, where XX in E, NE, N, NW, W, SW, S, SE')
    print('  f#, fire#:  Fire sub at given depth, from 1 to 3')


print("Sector hunt starts!")
while True:
    print()
    print(f"sub: N={se.sub_N} E={se.sub_E} dir={direction(se.sub_dir_N, se.sub_dir_E)} depth={se.sub_depth}")
    (_, infirerange) = se.get_dist()
    if infirerange:
        print("In fire range!")
    print(
        f"boat {se.b+1}: N={se.boat_N[se.b]} E={se.boat_E[se.b]} dir={direction(se.boat_dir_N[se.b], se.boat_dir_E[se.b])} speed={se.boat_speed[se.b]}")
    if se.moved:
        print("Boat already moved")
    if se.fired:
        print("Boat already fired")

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
        (dist, infirerange) = se.get_dist()
        print(f"Distance: {dist}")
        if infirerange:
            print("In fire range!")
        continue

    if ma := re.fullmatch(r"(s|speed) *([0-9])", rep):
        s = int(ma.group(2))
        if se.set_speed(s):
            print("Speed set successfully")
        else:
            print("Error setting speed")
        continue

    if ma := re.fullmatch(r"(d|dir) *(e|ne|n|nw|w|sw|s|se)", rep):
        dir = str.lower(ma.group(2))
        ddir_N = {'e': 0, 'ne': 1, 'n': 1, 'nw': 1, 'w': 0, 'sw': -1, 's': -1, 'se': -1}
        ddir_E = {'e': 1, 'ne': 1, 'n': 0, 'nw': -1, 'w': -1, 'sw': -1, 's': 0, 'se': 1}
        dir_N = ddir_N.get(dir, -2)
        dir_E = ddir_E.get(dir, -2)
        if se.set_dir(dir_N, dir_E):
            print("Direction set successfully")
        else:
            print("Error setting direction")
        continue

    if rep == 'm' or rep == 'move':
        (status, success) = se.move()
        if success:
            print("Boat moved successfully")
        else:
            print(f"Error moving boat: {status}")
        continue

    if ma := re.fullmatch(r"(f|fire) *(e|ne|n|nw|w|sw|s|se)", rep):
        dir = str.lower(ma.group(2))
        ddir_N = {'e': 0, 'ne': 1, 'n': 1, 'nw': 1, 'w': 0, 'sw': -1, 's': -1, 'se': -1}
        ddir_E = {'e': 1, 'ne': 1, 'n': 0, 'nw': -1, 'w': -1, 'sw': -1, 's': 0, 'se': 1}
        dir_N = ddir_N.get(dir, -2)
        dir_E = ddir_E.get(dir, -2)
        if se.set_fire_dir(dir_N, dir_E):
            print("Fire direction set successfully")
        else:
            print("Error setting fire direction")
        continue

    if ma := re.fullmatch(r"(f|fire) *([1-3])", rep):
        depth = int(ma.group(2))
        (status, success) = se.fire(depth)
        if success:
            print("Fire result: ", status)
        else:
            print("Error firing: ", status)
        continue

    if ma := re.fullmatch(r"(j|jump) *(\d\d)(,|( +))(\d\d)", rep):
        new_N = int(ma.group(2))
        new_E = int(ma.group(5))
        if se.jump(new_N, new_E):
            print('Jump successful')
        else:
            print('Jump failed')
        continue

    print("Unknown command, enter h for help")
