# ano2.py
# New type annotations exercices on classes
# 2021-04-11    PV


class Actor:
    def __init__(self, name:str) -> None:
        self.name = name

    def print_name(self):
        print(self.name)


class MobileActor(Actor):
    def __init__(self, name:str, max_speed:float) -> None:
        super().__init__(name)
        self.max_speed = max_speed
        self.speed: float

    def set_speed(self, speed: float) -> bool:
        if speed<=self.max_speed:
            self.speed = speed
            return True
        return False

class Car(MobileActor):
    def __init__(self, name: str, max_speed: float, color: str) -> None:
        super().__init__(name, max_speed)
        self.color = color

    def honk(self):
        print(f'Honk from car {self.name}')


class Action:
    def __init__(self, a:Actor) -> None:
        self.actor = a

class MobileAction(Action):
    def __init__(self, a: MobileActor) -> None:
        super().__init__(a)
        self.actor: MobileActor     # retag using derived type

    def stop(self) -> None:
        self.actor.speed = 0

class Unrelated:
    pass

u = Unrelated()
c1 = Car('Car #1', 25, 'Red')
ma1 = MobileAction(c1)
