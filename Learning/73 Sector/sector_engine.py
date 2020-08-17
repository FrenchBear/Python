# sector_engine
# simulation du jeu sector, coeur sans interface
# 2020-08-17    PV

from random import randint

class sector_engine:
    def __init__(self) -> None:
        self.sub_depth = randint(1,3)
        self.sub_E = randint(25, 75)
        self.sub_N = randint(25, 75)
        self.sub_dir = randint(0,7)     # 0=E, 1=NE, 2=N, 3=NW, 4=W, 5=SW, 6=S, 7=SE

        self.b = 0
        self.boat_E = [25, 25, 30, 35]
        self.boat_N = [35, 30, 25, 25]
        self.boat_dir = [1, 1, 1, 1]
        self.boat_speed = [0, 0, 0, 0]

    def get_dist(self) -> int:
        d = max(abs(self.sub_N-self.boat_N[self.b]), abs(self.sub_E-self.boat_E[self.b]))
        return d




# tests
se = sector_engine()

print(f"sub: N={se.sub_N} E={se.sub_E} dir={se.sub_dir} depth={se.sub_depth}")
for b in range(4):
    print(f"boat {b+1}: N={se.boat_N[b]} E={se.boat_E[b]} dir={se.boat_dir[b]} speed={se.boat_speed[b]}")

print()
print(f"Current boat: {se.b+1}")
print(f"Distance: {se.get_dist()}")
