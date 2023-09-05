# Classic coroutine averager
# Eample 17-37..39

from collections.abc import Generator

def averager() -> Generator[float, float, None]:
    total = 0.0
    count = 0
    average = 0.0
    while True:
        term = yield average
        total += term
        count += 1
        average = total/count

avg=averager()
next(avg)
print(avg.send(10))
print(avg.send(30))
print(avg.send(5))
avg.close()
