# Static vs Class vs Instance Methods in Python
# 2018-06-20 PV
class Sprocket:
    # Instance method (constructor)
    def __init__(self, name):
        # Instance variable
        self.Name = name

    # Instance Method
    def GetName(self):
        return self.Name

    # Class variable
    count = 0

    @classmethod
    def Increment(cls):
        cls.count+=1

    @classmethod
    def GetCount(cls):
        return cls.count

    @staticmethod
    def StaticMethod():
        print("Hello from StaticMethod: ", Sprocket.count)



s1 = Sprocket("one")
s2 = Sprocket("two")

print(s1.GetName())
print(s2.GetName())

Sprocket.Increment()
Sprocket.Increment()
print(Sprocket.GetCount())

s1.StaticMethod()
Sprocket.StaticMethod()
