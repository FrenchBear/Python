def f3(p: Any) -> None:
    ...

o0 = object()
o1 = T1()
o2 = T2()

f3(o0)  #
f3(o1)  #  all OK: rule #2
f3(o2)  #

def f4():  # implicit return type: `Any`
    ...

o4 = f4()  # inferred type: `Any`

f1(o4)  #
f2(o4)  #  all OK: rule #3
f3(o4)  #
