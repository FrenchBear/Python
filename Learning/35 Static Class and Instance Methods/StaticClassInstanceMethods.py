# Static vs Class vs Instance Methods in Python
# With classmethods, the class of the object instance is implicitly passed as the first argument instead of self.
# With staticmethods, neither self (the object instance) nor cls (the class) is implicitly passed as the first argument.
# They behave like plain functions except that you can call them from an instance or the class.
#
# 2018-06-20    PV
# 2018-08-20    PV      Added python documentation text
# 2018-12-16	PV	    Example of instance method using this instead of self

"""
Built-in @classmethod
    Transform a method into a class method.

    A class method receives the class as implicit first argument, just like an instance method receives the instance. 
    To declare a class method, use this idiom:

    class C:
        @classmethod
        def f(cls, arg1, arg2, ...): ...

    The @classmethod form is a function decorator – see the description of function definitions in Function definitions for details.

    It can be called either on the class (such as C.f()) or on an instance (such as C().f()). The instance is ignored except for its class. 
    If a class method is called for a derived class, the derived class object is passed as the implied first argument.

    Class methods are different than C++ or Java static methods. If you want those, see staticmethod() in this section.

    For more information on class methods, consult the documentation on the standard type hierarchy in The standard type hierarchy.
"""

"""
Built-in @staticmethod
    Transform a method into a static method.

    A static method does not receive an implicit first argument. To declare a static method, use this idiom:

    class C:
        @staticmethod
        def f(arg1, arg2, ...): ...

    The @staticmethod form is a function decorator – see the description of function definitions in Function definitions for details.

    It can be called either on the class (such as C.f()) or on an instance (such as C().f()). The instance is ignored except for its class.

    Static methods in Python are similar to those found in Java or C++. Also see classmethod() for a variant that is useful
    for creating alternate class constructors.

    Like all decorators, it is also possible to call staticmethod as a regular function and do something with its result. 
    This is needed in some cases where you need a reference to a function from a class body and you want to avoid the automatic transformation
    to instance method. For these cases, use this idiom:

    class C:
        builtin_open = staticmethod(open)

    For more information on static methods, consult the documentation on the standard type hierarchy in The standard type hierarchy.
"""

class Sprocket:
    # Instance method (constructor)
    def __init__(self, name):
        # Instance variable
        self.Name = name

    # Instance Method
    def GetName(self):
        return self.Name

    # Variant of class method using this.  Pylint complains about it, but python interpreter is Ok.
    def GetName2(this):
        return this.Name

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
print(s1.GetName2())            # Instance method with this instead of self

Sprocket.Increment()
Sprocket.Increment()
print("Call class method from class: ", Sprocket.GetCount())
print("Call class method from instance: ", s1.GetCount())

# Call static method from class
Sprocket.StaticMethod()
# Call static method from instance
s1.StaticMethod()
