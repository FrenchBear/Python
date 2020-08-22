# sector_engine.py
# Sector game simulation, core game engine (no interface)
# 2020-08-17    PV

import math
from random import randint
from typing import Tuple


class sector_engine:
    def __init__(self) -> None:
        self.new_game()

    def new_game(self):
        #self.sub_dir_N = self.sub_dir_E = 0
        self.init_sub_random()
        self.b = 0
        self.boat_N = [35, 30, 25, 25]
        self.boat_E = [25, 25, 30, 35]
        self.boat_dir_N = [1, 1, 1, 1]
        self.boat_dir_E = [1, 1, 1, 1]
        self.boat_speed = [0, 0, 0, 0]
        self.moved = False
        self.fired = False
        self.fire_dir_N = 0
        self.fire_dir_E = 1
        self.sub_evasive = False

    # Conversion helper (dir_N, dir_E)->dir
    def NE_dir(self, dir_N: int, dir_E: int) -> int:
        a = int(round(math.atan2(dir_N, dir_E)/math.pi*180/45, 0))
        return (a+8) % 8

    # Conversion helper dir->(dir_N, dir_E)
    def dir_NE(self, dir: int) -> Tuple[int, int]:
        a = dir*math.pi/4
        dir_N = int(round(math.sin(a), 0))
        dir_E = int(round(math.cos(a), 0))
        return dir_N, dir_E

    # Sub direction based on compass model 0=E, 1=NE, ...
    def get_sub_dir(self) -> int:
        return self.NE_dir(self.sub_dir_N, self.sub_dir_E)

    def set_sub_dir(self, dir: int):
        (self.sub_dir_N, self.sub_dir_E) = self.dir_NE(dir)

    def init_sub_random(self):
        self.sub_depth = randint(1, 3)
        while True:
            self.sub_E = randint(30, 70)
            self.sub_N = randint(30, 70)
            # To simplify sub rebound on 30/70 border, don't allow main diagonals that cause complex rebound on corners
            if self.sub_N != self.sub_E and 100-self.sub_N != self.sub_E:
                break
        self.set_sub_dir(randint(0, 7))

    def teach_mode(self):
        self.new_game()
        self.sub_N = 35
        self.sub_E = 35
        self.set_sub_dir(1)
        self.sub_depth = 1

    def set_evasive_mode(self):
        self.sub_evasive = True

    # Returns distance of current boat to sub, and a boolean True if in firing range
    def get_range(self) -> Tuple[int, bool]:
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

        # Sub only navigates between coord 30 and 70 on both directions
        # When bouncing on 30/70 border, perpendicular direction changes randomly
        if (self.sub_N == 30 and self.sub_dir_N < 0) or (self.sub_N == 70 and self.sub_dir_N > 0):
            self.sub_dir_N = -self.sub_dir_N
            self.sub_dir_E = randint(-1, 1)
        if (self.sub_E == 30 and self.sub_dir_E < 0) or (self.sub_E == 70 and self.sub_dir_E > 0):
            self.sub_dir_E = -self.sub_dir_E
            self.sub_dir_N = randint(-1, 1)

        self.sub_N += self.sub_dir_N
        self.sub_E += self.sub_dir_E

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

        # Move 1 cell at a time to detect collisions
        new_N = self.boat_N[self.b]
        new_E = self.boat_E[self.b]
        for i in range(1, self.boat_speed[self.b]+1):
            new_N = self.boat_N[self.b] + i*self.boat_dir_N[self.b]
            new_E = self.boat_E[self.b] + i*self.boat_dir_E[self.b]
            if self.occupied(new_N, new_E):
                # Bump from colision point
                self.boat_N[self.b] = new_N
                self.boat_E[self.b] = new_E
                self.bump()
                return ('Collision!  Bumped!', False)

        # Can't play out of 20-80 grid
        if not (20 <= new_N <= 80 and 20 <= new_E <= 80):
            return ("Can't move outside of 20-80 grid", False)

        self.moved = True
        self.boat_N[self.b] = new_N
        self.boat_E[self.b] = new_E
        return ('', True)

    # Returns False if there is a problem (fire direction unchanged), True if fire direction has been set
    def set_fire_dir(self, fire_N: int, fire_E: int) -> bool:
        if isinstance(fire_N, int) and -1 <= fire_N <= 1 and isinstance(fire_E, int) and -1 <= fire_E <= 1 and abs(fire_E)+abs(fire_N) != 0:
            self.fire_dir_N = fire_N
            self.fire_dir_E = fire_E
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
                (dist, canfire) = self.get_range()
                if not canfire:
                    self.bump()
                    return ('Not in firing range, bumped!', False)

                # Check that direction is correct
                if self.boat_N[self.b] + self.fire_dir_N*dist != self.sub_N or self.boat_E[self.b] + self.fire_dir_E*dist != self.sub_E:
                    self.bump()
                    if self.set_evasive_mode():
                        self.sub_changecap()
                    return('Fired in wrong direction, bumped!', False)

                # Check depth
                if self.sub_depth == depth:
                    self.init_sub_random()
                    return('Sumbarine hit! You won!  New sub position generated', True)

                if self.set_evasive_mode():
                    self.sub_changecap()
                return(f'Almost hit submarine! Depth offset={abs(self.sub_depth-depth)}', True)

        return ('Arg err', False)

    # sub can turn left 45°, right 45°, or not
    def sub_changecap(self):
        dir = (self.get_sub_dir()+randint(-1, 1)+8) % 8
        self.set_sub_dir(dir)

    def bump(self):
        while True:
            # Chose random direction, keep speed
            while True:
                self.boat_dir_N[self.b] = randint(-1, 1)
                self.boat_dir_E[self.b] = randint(-1, 1)
                if self.boat_dir_N[self.b] != 0 or self.boat_dir_E[self.b] != 0:
                    break
            new_N = self.boat_N[self.b] + self.boat_dir_N[self.b]*self.boat_speed[self.b]
            new_E = self.boat_E[self.b] + self.boat_dir_E[self.b]*self.boat_speed[self.b]
            if not self.occupied(new_N, new_E) and 20 <= new_N <= 80 and 20 <= new_E <= 80:
                self.boat_N[self.b] = new_N
                self.boat_E[self.b] = new_E
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
