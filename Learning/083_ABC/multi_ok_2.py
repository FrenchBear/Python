# This works, because neither base classes of B class use super()
# 2021-05-08    PV

class A1:
    def __init__(self) -> None:
        print('A1')

class A2:
    def __init__(self) -> None:
        print('A2')

class B(A1, A2):
    def __init__(self) -> None:
        print('B')
        A1.__init__(self)
        A2.__init__(self)

b = B()
