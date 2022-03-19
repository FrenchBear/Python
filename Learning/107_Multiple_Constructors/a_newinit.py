# Play with Python contructors
# 01 Refresher about __new__ and __init__
#
# 2022-03-19    PV

# A base class is object, identical to class A(object):
class A:
    def __new__(cls):
         print("Creating instance of A")
         return super(A, cls).__new__(cls)
  
    # Should return None
    def __init__(self):
        print("A Init is called")
  
A()
print()

class B:
    # Actually, __new__ can return anything...
    def __new__(cls):
         print("Creating instance of B")
         return "Hello world"

    # Note that __init__ is not called, since __new__ did not return a __B__ object
    def __init__(self):
        print("B Init is called")

b = B() 
print(b)

