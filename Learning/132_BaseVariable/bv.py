# BaseVariable.py
# From XKCD #2835   https://xkcd.com/2835/
#
# 2023-10-10    PV

def DecToBV(n: int) -> str:
    f = 2
    r = 2
    while n >= f:
        r += 1
        f *= r
    res = ''
    while r>1:
        f //= r
        r -= 1
        d,n = divmod(n, f)
        res += str(d)
    return res

print(DecToBV(25))
