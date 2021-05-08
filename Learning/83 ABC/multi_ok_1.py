# Working example with multiple inheritance
# 2021-05-08    PV

class Animal:
  def __init__(self, animalName):
    print(animalName, 'is an animal.')

# Mammal inherits Animal
class Mammal(Animal):
  def __init__(self, mammalName):
    print(mammalName, 'is a mammal.')
    super().__init__(mammalName)
    
# CannotFly inherits Mammal
class CannotFly(Mammal):
  def __init__(self, mammalThatCantFly):
    print(mammalThatCantFly, "cannot fly.")
    super().__init__(mammalThatCantFly)

# CannotSwim inherits Mammal
class CannotSwim(Mammal):
  def __init__(self, mammalThatCantSwim):
    print(mammalThatCantSwim, "cannot swim.")
    super().__init__(mammalThatCantSwim)

# Cat inherits CannotSwim and CannotFly
class Cat(CannotSwim, CannotFly):
  def __init__(self):
    print('I am a cat.')
    super().__init__('Cat')

# Driver code
cat = Cat()
print('')
bat = CannotSwim('Bat')
