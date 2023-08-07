# Example 13-8

from tombola import Tombola
class Fake(Tombola):
    def pick(self):
        return 13

f = Fake()
