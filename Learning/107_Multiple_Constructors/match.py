class Point:
    x: int
    y: int
    __match_args__ = ('x', 'y')

    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f'Point({self.x}, {self.y})'

points = [Point(0,0), Point(0,3)]
print(points)

match points:
    case []:
        print('Empty list')
    case [Point()]:
        print('List of 1 Point')
    case [Point(), Point()]:
        print('List of 2 Points')

match points:
    case []:
        print('Empty list')
    case [Point(0,0)]:
        print('List of 1 Point')
    case [Point(a,b), Point(c,d)]:
        print(f'List of 2 Points ({a}, {b}), ({c}, {d})')

match points:
    case []:
        print('Empty list')
    case [X]:
        print('List of 1 item')
    case [X, Y]:
        print(f'List of 2 items {X}, {Y}')

match points:
    case []:
        print('Empty list')
    case [Point() as P1]:
        print('List of 1 Point')
    case [Point() as P1, Point() as P2]:
        print(f'List of 2 Points {P1}, {P2}')

match points:
    case []:
        print('Empty list')
    case [Point(a,b) as P1]:
        print('List of 1 Point')
    case [Point(a,b) as P1, Point(c,d) as P2]:
        print(f'List of 2 Points P1:({a}, {b})={P1}, P2:({c}, {d})={P2}')
