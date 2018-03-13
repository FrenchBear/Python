
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
        return "Dog({},{})".format(repr(self.color),repr(self.name))
    
    def __str__(self):
        return "I am a {} Dog named {}.".format(self.color,self.name)

shelly = Dog('white', 'Shelly')
print(shelly)
print(repr(shelly))

