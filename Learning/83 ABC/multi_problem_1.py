# multi_problem_1: Problems caused by inconsistent use of super()
# In this example, since base classes A1 and A2 do not call super().__init but B does, only A1 constructor get called
# 2021-05-08    PV

class A1:
    def __init__(self) -> None:
        print('A1 init')
        #super().__init__()


class A2:
    def __init__(self) -> None:
        print('A2 init')
        #super().__init__()


class B(A1, A2):
    def __init__(self) -> None:
        print('B init')
        super().__init__()

b = B()
