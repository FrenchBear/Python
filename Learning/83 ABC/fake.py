# test of a bad implementation of tombola
# 2021-04-28    PV

from tombola import Tombola

class Fake(Tombola):
    def pick(self):
        return 13

if __name__=='__maim__':
    """ Exception has occurred: TypeError
        Can't instantiate abstract class Fake with abstract method load
    """
    # f = Fake()
