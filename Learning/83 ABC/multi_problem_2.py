# multi_problem_2: Problems caused by inconsistent use of super()
# From https://fuhm.net/super-harmful/
# Base class gets called twice if parent class uses super() but not derived class
# 2021-05-08    PV

class A:
    def __init__(self):
        print("A")
        super().__init__()

class B:
    def __init__(self):
        print("B")
        super().__init__()

# some other module defines this class, not knowing about super()
class C(A, B):
    def __init__(self):
        print("C")
        # Next two lines calls B.__init__ twice
        A.__init__(self)
        B.__init__(self)
        # This instead calls B only once
        # super().__init__()


print("MRO:", [x.__name__ for x in C.__mro__])
C()
