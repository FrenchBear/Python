# Static vs Class vs Instance Methods in Python
# With classmethods, the class of the object instance is implicitly passed as the first argument instead of self.
# With staticmethods, neither self (the object instance) nor cls (the class) is implicitly passed as the first argument.
# They behave like plain functions except that you can call them from an instance or the class.
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
        cls.count += 1

    @classmethod
    def GetCount(cls):
        return cls.count

    @staticmethod
    def StaticMethod():
        print("Hello from StaticMethod: ", Sprocket.count)


s1 = Sprocket("one")
s2 = Sprocket("two")

# Call instance method from object
print(s1.GetName())             # Usual dotted syntax
print(Sprocket.GetName(s2))     # Function-style call from class, passing object as 1st parameter

Sprocket.Increment()
Sprocket.Increment()
print("Call class method from class: ", Sprocket.GetCount())
print("Call class method from instance: ", s1.GetCount())

# Call static method from class
Sprocket.StaticMethod()
# Call static method from instance
s1.StaticMethod()
