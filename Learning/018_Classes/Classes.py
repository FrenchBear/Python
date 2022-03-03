# 18 Classes
# Learning Python, playing with classes
#
# 2015-07-14    PV
# 2022-03-03    PV      Replaced __new__ by __init__

class animal:
    def __init__(self, name):
        self.name = name

    def Name(self):
        return self.name


a = animal('King Kong')
print(a.Name())
