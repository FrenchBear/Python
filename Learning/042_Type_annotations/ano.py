# Type annotations
# Exercices on Pyhton 3.7 and mypy
#
# This file generates error when checked using mypy, this is normal and on purpose!!!
#
# 2008-08-24    PV

from typing import Dict, List, Union


class Dog:
    def __init__(self, name):
        self.nom = name

    def aboie(self):
        print(self.nom + ": Ouah!")


class Cat:
    def __init__(self, name):
        self.nom = name

    def miaule(self):
        print(self.nom + ": Miaou!")


import datetime


class Album:
    def __init__(self, title, artist, release_year, tracks):
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks = tracks

    def all_tracks_shorter_than(self, minutes=0, seconds=0):
        duration = datetime.timedelta(minutes=minutes, seconds=seconds)
        return [t for t in self.tracks if t.duration < duration]


class Track:
    def __init__(self, title, duration):
        self.title = title
        self.duration = duration


def excite(a: Dog):
    a.aboie()
    print(a.nom)
    a.aboie()


medor = Dog("Medor")
excite(medor)

# mypy will detect the problem calling excite with a Dog
felix = Cat("Félix")
# excite(felix)


def get_first_name(full_name: str) -> str:
    return full_name.split(" ")[0]


fallback_name: Dict[str, str] = {
    "first_name": "UserFirstName",
    "last_name": "UserLastName"
}

raw_name: str = input("Please enter your name: ")
first_name: str = get_first_name(raw_name)

# If the user didn't type anything in, use the fallback name
if not first_name:
    first_name = get_first_name(fallback_name)      # Error since fallbackname is a dictionary!
# mypy: ano.py:73: error: Argument 1 to "get_first_name" has incompatible type "Dict[str, str]"; expected "str"

print(f"Hi, {first_name}!")

i: int = 0
l: List[int] = [1, 2, 3]


def myfunc() -> List[int]:
    return [1, 2, 3]


class myclass:
    def myfunc(self, s: str) -> List[int]:
        return [1, 2, 3]


l = myfunc()

cc = myclass()
l = cc.myfunc("zap")


zs: Union[str, int] 
zs = 3
zs = 'top'
# zs=3.13        # Error float type


# def triple(x:Union[str,int]) -> Union[str,int]:
def triple(x:Union[str, int]):
    return x+x+x
# mypy: ano.py:104: error: Unsupported operand types for + ("str" and "int")
# mypy: ano.py:104: error: Unsupported operand types for + ("int" and "str")
# mypy: ano.py:104: note: Both left and right operands are unions

print(triple(2))
print(triple('ga'))
print(triple(3.13))     # Not good
# mypy: ano.py:109: error: Argument 1 to "triple" has incompatible type "float"; expected "Union[str, int]"
