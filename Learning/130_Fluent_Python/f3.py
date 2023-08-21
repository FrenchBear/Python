
from typing import Any, Self


class Thing:
    def __init__(self, v: int) -> None:
        self.v = v

    # def __getattribute__(self, __name: str) -> Any:
    #     print("__getattribute__", str)
    #     return None

    # def __getitem__(self, index: Any) -> Any:
    #     print("__getitem__", str)
    #     return None

    # def __call__(self, *args: Any, **kwargs: Any) -> Any:
    #     print("__call__", args, kwargs)
    #     return None

    def __gt__(self, other: Self) -> bool:
        return self.v > other.v

    def __le__(self, other: Self) -> bool:
        return self.v <= other.v


t2 = Thing(2)
# print(t2.color)
# print(t2["red"])
# print(t2(2, temp="Cold"))

t5 = Thing(5)

print(t2 > t5)
print(t2 <= t5)
