
class Animal:
    def __init__(self, n_legs, color):
        self.n_legs = n_legs
        self.color = color

    def make_noise(self):
        print('noise')


class Dog(Animal):
    def __init__(self, color, name):
        Animal.__init__(self, 4, color)
        self.name = name

    def make_noise(self):
        print((self.name + ': ' + 'woof'))

    def __repr__(self):
        return "Dog({},{})".format(repr(self.color), repr(self.name))
    
    def __str__(self):
        return "I am a {} Dog named {}.".format(self.color, self.name)

    # No default implem for len(Dog)
    def __len__(self):
        return len(self.name)

    def __eq__(self, other):
        if type(other) is not type(self): return False
        return self.name == other.name


shelly = Dog('white', 'Shelly')
print(shelly)
print(repr(shelly))
print(len(shelly))

kafi_f = Dog('fauve', 'Kafi')
kafi_b = Dog('black', 'Kafi')

print(shelly == None)
print(shelly == 3)
print(shelly == kafi_f)
print(kafi_f == kafi_b)

print()

# __ne__ is automatically generated
print(shelly != kafi_f)
print(kafi_f != kafi_b)

