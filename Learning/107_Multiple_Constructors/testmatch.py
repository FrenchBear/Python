# tests on match operation of Python 3.10
#
# 2022-03-19    PV


class Point2D:
    __match_args__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point2D({self.x}, {self.y})'


class Point3D:
    __match_args__ = ("x", "y", "z")

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f'Point3D({self.x}, {self.y}, {self.z})'


p1 = Point2D(2,3)
p2 = Point3D(3,-1,2)

print(p1)
print(p2)


match p2:
    case Point2D(x, y):
        print(f"Match Point2D: x={x}, y={y}")
    case Point3D(x, y, z):
        print(f"Match Point3D: x={x}, y={y}, z={z}")
    case _:
        print('No match')
